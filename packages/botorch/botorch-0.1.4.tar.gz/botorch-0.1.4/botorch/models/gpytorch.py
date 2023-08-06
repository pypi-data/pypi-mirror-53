#! /usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

r"""
Abstract model class for all GPyTorch-based botorch models.

To implement your own, simply inherit from both the provided classes and a
GPyTorch Model class such as an ExactGP.
"""

import warnings
from abc import ABC, abstractproperty
from contextlib import ExitStack
from typing import Any, List, Optional, Tuple

import torch
from gpytorch import settings as gpt_settings
from gpytorch.distributions import MultitaskMultivariateNormal, MultivariateNormal
from gpytorch.lazy import lazify
from gpytorch.likelihoods.gaussian_likelihood import FixedNoiseGaussianLikelihood
from torch import Tensor

from .. import settings
from ..exceptions.errors import BotorchTensorDimensionError
from ..exceptions.warnings import BotorchTensorDimensionWarning
from ..posteriors.gpytorch import GPyTorchPosterior
from .model import Model
from .utils import _make_X_full, add_output_dim, multioutput_to_batch_mode_transform


class GPyTorchModel(Model, ABC):
    r"""Abstract base class for models based on GPyTorch models.

    The easiest way to use this is to subclass a model from a GPyTorch model
    class (e.g. an `ExactGP`) and this `GPyTorchModel`. See e.g. `SingleTaskGP`.
    """

    @staticmethod
    def _validate_tensor_args(
        X: Tensor, Y: Tensor, Yvar: Optional[Tensor] = None, strict: bool = True
    ) -> None:
        r"""Checks that `Y` and `Yvar` have an explicit output dimension if strict.

        This also checks that `Yvar` has the same trailing dimensions as `Y`. Note
        we only infer that an explicit output dimension exists when `X` and `Y` have
        the same `batch_shape`.

        Args:
            X: A `n x d` or `batch_shape x n x d`-dim Tensor, where `d` is the
                dimension of the feature space, `n` is the number of points per
                batch, and `batch_shape` is the batch shape.
            Y: A `n x m` or `batch_shape x n x m`-dim Tensor, where `m` is the
                number of model outputs, `n'` is the number of points per batch,
                and `batch_shape'` is the batch shape of the observations.
            Yvar: A `n x m` or `batch_shape x n x m` (batch mode) tensor of
                observed measurement noise. Note: this will be None when using a
                model that infers the noise level (e.g. a `SingleTaskGP`).
            strict: A boolean indicating whether to check that `Y` and `Yvar` have
                an explicit output dimension.
        """
        if strict:
            if X.dim() != Y.dim():
                if (X.dim() - Y.dim() == 1) and (X.shape[:-1] == Y.shape):
                    message = (
                        "An explicit output dimension is required for targets."
                        f" Expected Y with dimension: {Y.dim()} (got {X.dim()})."
                    )
                else:
                    message = (
                        f"Expected X and Y to have the same number of dimensions"
                        f" (got X with dimension {X.dim()} and Y with dimension"
                        f" {Y.dim()}."
                    )
                raise BotorchTensorDimensionError(message)
        else:
            warnings.warn(
                "Non-strict enforcement of botorch tensor conventions. Ensure that "
                f"target tensors Y{' and Yvar have' if Yvar is not None else ' has an'}"
                f" explicit output dimension{'s' if Yvar is not None else ''}.",
                BotorchTensorDimensionWarning,
            )
        # Yvar may not have the same batch dimensions, but the trailing dimensions
        # of Yvar should be the same as the trailing dimensions of Y.
        if Yvar is not None and Y.shape[-Yvar.dim() :] != Yvar.shape:
            raise BotorchTensorDimensionError(
                "An explicit output dimension is required for observation noise."
                f" Expected Yvar with shape: {Y.shape[-Yvar.dim() :]} (got"
                f" {Yvar.shape})."
            )

    def posterior(
        self, X: Tensor, observation_noise: bool = False, **kwargs: Any
    ) -> GPyTorchPosterior:
        r"""Computes the posterior over model outputs at the provided points.

        Args:
            X: A `(batch_shape) x q x d`-dim Tensor, where `d` is the dimension of the
                feature space and `q` is the number of points considered jointly.
            observation_noise: If True, add observation noise to the posterior.

        Returns:
            A `GPyTorchPosterior` object, representing a batch of `b` joint
            distributions over `q` points. Includes observation noise if
            `observation_noise=True`.
        """
        self.eval()  # make sure model is in eval mode
        with ExitStack() as es:
            es.enter_context(gpt_settings.debug(False))
            es.enter_context(gpt_settings.fast_pred_var())
            es.enter_context(
                gpt_settings.detach_test_caches(settings.propagate_grads.off())
            )
            mvn = self(X)
            if observation_noise:
                # TODO: Allow passing in observation noise via kwarg
                mvn = self.likelihood(mvn, X)
            return GPyTorchPosterior(mvn=mvn)

    def condition_on_observations(self, X: Tensor, Y: Tensor, **kwargs: Any) -> "Model":
        r"""Condition the model on new observations.

        Args:
            X: A `batch_shape x n' x d`-dim Tensor, where `d` is the dimension of
                the feature space, `n'` is the number of points per batch, and
                `batch_shape` is the batch shape (must be compatible with the
                batch shape of the model).
            Y: A `batch_shape' x n x m`-dim Tensor, where `m` is the number of
                model outputs, `n'` is the number of points per batch, and
                `batch_shape'` is the batch shape of the observations.
                `batch_shape'` must be broadcastable to `batch_shape` using
                standard broadcasting semantics. If `Y` has fewer batch dimensions
                than `X`, its is assumed that the missing batch dimensions are
                the same for all `Y`.

        Returns:
            A `Model` object of the same type, representing the original model
            conditioned on the new observations `(X, Y)` (and possibly noise
            observations passed in via kwargs).

        Example:
            >>> train_X = torch.rand(20, 2)
            >>> train_Y = torch.sin(train_X[:, 0]) + torch.cos(train_X[:, 1])
            >>> model = SingleTaskGP(train_X, train_Y)
            >>> new_X = torch.rand(5, 2)
            >>> new_Y = torch.sin(new_X[:, 0]) + torch.cos(new_X[:, 1])
            >>> model = model.condition_on_observations(X=new_X, Y=new_Y)
        """
        noise = kwargs.get("noise", None)
        # validate using strict=False, since we cannot tell if Y has an explicit
        # output dimension
        self._validate_tensor_args(X=X, Y=Y, Yvar=noise, strict=False)
        if Y.shape[-1] == 1:
            targets = Y.squeeze(-1)
            if noise is not None:
                kwargs.update({"noise": noise.squeeze(-1)})
        else:
            targets = Y
        return self.get_fantasy_model(inputs=X, targets=targets, **kwargs)


class BatchedMultiOutputGPyTorchModel(GPyTorchModel):
    r"""Base class for batched multi-output GPyTorch models with independent outputs.

    This model should be used when the same training data is used for all outputs.
    Outputs are modeled independently by using a different batch for each output.
    """

    _num_outputs: int
    _input_batch_shape: torch.Size
    _aug_batch_shape: torch.Size

    def _set_dimensions(self, train_X: Tensor, train_Y: Tensor) -> None:
        r"""Store the number of outputs and the batch shape.

        Args:
            train_X: A `n x d` or `batch_shape x n x d` (batch mode) tensor of training
                features.
            train_Y: A `n x m` or `batch_shape x n x m` (batch mode) tensor of
                training observations.
        """
        self._num_outputs = train_Y.shape[-1]
        self._input_batch_shape = train_X.shape[:-2]
        self._aug_batch_shape = self._input_batch_shape
        if self._num_outputs > 1:
            self._aug_batch_shape += torch.Size([self._num_outputs])

    def _transform_tensor_args(
        self, X: Tensor, Y: Tensor, Yvar: Optional[Tensor] = None
    ) -> Tuple[Tensor, Tensor, Optional[Tensor]]:
        r"""Transforms tensor arguments: for single output models, the output
        dimension is squeezed and for multi-output models, the output dimension is
        transformed into the left-most batch dimension.

        Args:
            X: A `n x d` or `batch_shape x n x d` (batch mode) tensor of training
                features.
            Y: A `n x m` or `batch_shape x n x m` (batch mode) tensor of
                training observations.
            Yvar: A `n x m` or `batch_shape x n x m` (batch mode) tensor of
                observed measurement noise. Note: this will be None when using a model
                that infers the noise level (e.g. a `SingleTaskGP`).

        Returns:
            3-element tuple containing

            - A `input_batch_shape x (m) x n x d` tensor of training features.
            - A `target_batch_shape x (m) x n` tensor of training observations.
            - A `target_batch_shape x (m) x n` tensor observed measurement noise
                (or None).
        """
        if self._num_outputs > 1:
            return multioutput_to_batch_mode_transform(
                train_X=X, train_Y=Y, train_Yvar=Yvar, num_outputs=self._num_outputs
            )
        return X, Y.squeeze(-1), None if Yvar is None else Yvar.squeeze(-1)

    def posterior(
        self,
        X: Tensor,
        output_indices: Optional[List[int]] = None,
        observation_noise: bool = False,
        **kwargs: Any,
    ) -> GPyTorchPosterior:
        r"""Computes the posterior over model outputs at the provided points.

        Args:
            X: A `(batch_shape) x q x d`-dim Tensor, where `d` is the dimension of the
                feature space and `q` is the number of points considered jointly.
            output_indices: A list of indices, corresponding to the outputs over
                which to compute the posterior (if the model is multi-output).
                Can be used to speed up computation if only a subset of the
                model's outputs are required for optimization. If omitted,
                computes the posterior over all model outputs.
            observation_noise: If True, add observation noise to the posterior.

        Returns:
            A `GPyTorchPosterior` object, representing `batch_shape` joint
            distributions over `q` points and the outputs selected by
            `output_indices` each. Includes observation noise if
            `observation_noise=True`.
        """
        self.eval()  # make sure model is in eval mode
        with ExitStack() as es:
            es.enter_context(gpt_settings.debug(False))
            es.enter_context(gpt_settings.fast_pred_var())
            es.enter_context(
                gpt_settings.detach_test_caches(settings.propagate_grads.off())
            )
            # insert a dimension for the output dimension
            if self._num_outputs > 1:
                X, output_dim_idx = add_output_dim(
                    X=X, original_batch_shape=self._input_batch_shape
                )
            mvn = self(X)
            if observation_noise:
                if isinstance(self.likelihood, FixedNoiseGaussianLikelihood):
                    # Use the mean of the previous noise values (TODO: be smarter here).
                    noise = self.likelihood.noise.mean().expand(X.shape[:-1])
                    mvn = self.likelihood(mvn, X, noise=noise)
                else:
                    mvn = self.likelihood(mvn, X)
            if self._num_outputs > 1:
                mean_x = mvn.mean
                covar_x = mvn.covariance_matrix
                output_indices = output_indices or range(self._num_outputs)
                mvns = [
                    MultivariateNormal(
                        mean_x.select(dim=output_dim_idx, index=t),
                        lazify(covar_x.select(dim=output_dim_idx, index=t)),
                    )
                    for t in output_indices
                ]
                mvn = MultitaskMultivariateNormal.from_independent_mvns(mvns=mvns)
        return GPyTorchPosterior(mvn=mvn)

    def condition_on_observations(
        self, X: Tensor, Y: Tensor, **kwargs: Any
    ) -> "BatchedMultiOutputGPyTorchModel":
        r"""Condition the model on new observations.

        Args:
            X: A `batch_shape x n' x d`-dim Tensor, where `d` is the dimension of
                the feature space, `m` is the number of points per batch, and
                `batch_shape` is the batch shape (must be compatible with the
                batch shape of the model).
            Y: A `batch_shape' x n' x m`-dim Tensor, where `m` is the number of
                model outputs, `n'` is the number of points per batch, and
                `batch_shape'` is the batch shape of the observations.
                `batch_shape'` must be broadcastable to `batch_shape` using
                standard broadcasting semantics. If `Y` has fewer batch dimensions
                than `X`, its is assumed that the missing batch dimensions are
                the same for all `Y`.

        Returns:
            A `BatchedMultiOutputGPyTorchModel` object of the same type with
            `n + n'` training examples, representing the original model
            conditioned on the new observations `(X, Y)` (and possibly noise
            observations passed in via kwargs).


        Example:
            >>> train_X = torch.rand(20, 2)
            >>> train_Y = torch.cat(
            >>>     [torch.sin(train_X[:, 0]), torch.cos(train_X[:, 1])], -1
            >>> )
            >>> model = SingleTaskGP(train_X, train_Y)
            >>> new_X = torch.rand(5, 2)
            >>> new_Y = torch.cat([torch.sin(new_X[:, 0]), torch.cos(new_X[:, 1])], -1)
            >>> model = model.condition_on_observations(X=new_X, Y=new_Y)
        """
        noise = kwargs.get("noise")
        self._validate_tensor_args(X=X, Y=Y, Yvar=noise, strict=False)
        inputs = X
        if self._num_outputs > 1:
            inputs, targets, noise = multioutput_to_batch_mode_transform(
                train_X=X, train_Y=Y, num_outputs=self._num_outputs, train_Yvar=noise
            )
            # `multioutput_to_batch_mode_transform` removes the output dimension,
            # which is necessary for `condition_on_observations`
            targets = targets.unsqueeze(-1)
            if noise is not None:
                noise = noise.unsqueeze(-1)
        else:
            inputs = X
            targets = Y
        if noise is not None:
            kwargs.update({"noise": noise})
        fantasy_model = super().condition_on_observations(X=inputs, Y=targets, **kwargs)
        fantasy_model._input_batch_shape = fantasy_model.train_targets.shape[
            : (-1 if self._num_outputs == 1 else -2)
        ]
        fantasy_model._aug_batch_shape = fantasy_model.train_targets.shape[:-1]
        return fantasy_model


class ModelListGPyTorchModel(GPyTorchModel, ABC):
    r"""Abstract base class for models based on multi-output GPyTorch models.

    This is meant to be used with a gpytorch ModelList wrapper for independent
    evaluation of submodels.
    """

    @abstractproperty
    def num_outputs(self) -> int:
        r"""The number of outputs of the model."""
        pass  # pragma: no cover

    def posterior(
        self,
        X: Tensor,
        output_indices: Optional[List[int]] = None,
        observation_noise: bool = False,
        **kwargs: Any,
    ) -> GPyTorchPosterior:
        r"""Computes the posterior over model outputs at the provided points.

        Args:
            X: A `b x q x d`-dim Tensor, where `d` is the dimension of the
                feature space, `q` is the number of points considered jointly,
                and `b` is the batch dimension.
            output_indices: A list of indices, corresponding to the outputs over
                which to compute the posterior (if the model is multi-output).
                Can be used to speed up computation if only a subset of the
                model's outputs are required for optimization. If omitted,
                computes the posterior over all model outputs.
            observation_noise: If True, add observation noise to the posterior.

        Returns:
            A `GPyTorchPosterior` object, representing `batch_shape` joint
            distributions over `q` points and the outputs selected by
            `output_indices` each. Includes measurement noise if
            `observation_noise=True`.
        """
        self.eval()  # make sure model is in eval mode
        with ExitStack() as es:
            es.enter_context(gpt_settings.debug(False))
            es.enter_context(gpt_settings.fast_pred_var())
            es.enter_context(
                gpt_settings.detach_test_caches(settings.propagate_grads.off())
            )
            if output_indices is not None:
                mvns = [self.forward_i(i, X) for i in output_indices]
                if observation_noise:
                    lh_kwargs = [
                        {"noise": lh.noise.mean().expand(X.shape[:-1])}
                        if isinstance(lh, FixedNoiseGaussianLikelihood)
                        else {}
                        for lh in self.likelihood.likelihoods
                    ]
                    mvns = [
                        self.likelihood_i(i, mvn, X, **lkws)
                        for i, mvn, lkws in zip(output_indices, mvns, lh_kwargs)
                    ]
            else:
                mvns = self(*[X for _ in range(self.num_outputs)])
                if observation_noise:
                    # TODO: Allow passing in observation noise via kwarg
                    mvns = self.likelihood(*[(mvn, X) for mvn in mvns])
        if len(mvns) == 1:
            return GPyTorchPosterior(mvn=mvns[0])
        else:
            return GPyTorchPosterior(
                mvn=MultitaskMultivariateNormal.from_independent_mvns(mvns=mvns)
            )

    def condition_on_observations(
        self, X: Tensor, Y: Tensor, **kwargs: Any
    ) -> "ModelListGPyTorchModel":
        raise NotImplementedError(
            "`condition_on_observations` not implemented in "
            "`ModelListGPyTorchModel` base class"
        )


class MultiTaskGPyTorchModel(GPyTorchModel, ABC):
    r"""Abstract base class for multi-task models baed on GPyTorch models.

    This class provides the `posterior` method to models that implement a
    "long-format" multi-task GP in the style of `MultiTaskGP`.
    """

    def posterior(
        self,
        X: Tensor,
        output_indices: Optional[List[int]] = None,
        observation_noise: bool = False,
        **kwargs: Any,
    ) -> GPyTorchPosterior:
        r"""Computes the posterior over model outputs at the provided points.

        Args:
            X: A `q x d` or `batch_shape x q x d` (batch mode) tensor, where `d` is the
                dimension of the feature space (not including task indices) and
                `q` is the number of points considered jointly.
            output_indices: A list of indices, corresponding to the outputs over
                which to compute the posterior (if the model is multi-output).
                Can be used to speed up computation if only a subset of the
                model's outputs are required for optimization. If omitted,
                computes the posterior over all model outputs.
            observation_noise: If True, add observation noise to the posterior.

        Returns:
            A `GPyTorchPosterior` object, representing `batch_shape` joint
            distributions over `q` points and the outputs selected by
            `output_indices`. Includes measurement noise if
            `observation_noise=True`.
        """
        if output_indices is None:
            output_indices = self._output_tasks
        if any(i not in self._output_tasks for i in output_indices):
            raise ValueError("Too many output indices")

        # construct evaluation X
        X_full = _make_X_full(X=X, output_indices=output_indices, tf=self._task_feature)

        self.eval()  # make sure model is in eval mode
        with ExitStack() as es:
            es.enter_context(gpt_settings.debug(False))
            es.enter_context(gpt_settings.fast_pred_var())
            es.enter_context(
                gpt_settings.detach_test_caches(settings.propagate_grads.off())
            )
            mvn = self(X_full)
            if observation_noise:
                # TODO: Allow passing in observation noise via kwarg
                mvn = self.likelihood(mvn, X_full)
        # If single-output, return the posterior of a single-output model
        if len(output_indices) == 1:
            return GPyTorchPosterior(mvn=mvn)
        # Otherwise, make a MultitaskMultivariateNormal out of this
        mtmvn = MultitaskMultivariateNormal(
            mean=mvn.mean.view(*X.shape[:-1], len(output_indices)),
            covariance_matrix=mvn.lazy_covariance_matrix,
            interleaved=False,
        )
        return GPyTorchPosterior(mvn=mtmvn)

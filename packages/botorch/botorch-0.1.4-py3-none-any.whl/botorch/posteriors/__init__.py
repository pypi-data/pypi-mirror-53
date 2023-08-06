#! /usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

from .gpytorch import GPyTorchPosterior
from .posterior import Posterior


__all__ = ["GPyTorchPosterior", "Posterior"]

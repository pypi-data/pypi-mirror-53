# -*- coding: utf-8 -*-
#
# Copyright 2018  Ternaris.
# SPDX-License-Identifier: Apache-2.0

"""Compatibility with older Python versions.

The smallest supported version is Python 3.5
"""

import functools
import sys
from pathlib import Path


if sys.version_info < (3, 6):
    _open = open  # pylint: disable=invalid-name

    @functools.wraps(_open)
    def open(path, *args, **kw):  # pylint: disable=missing-docstring
        if isinstance(path, Path):
            path = str(path)
        return _open(path, *args, **kw)

    from os import chmod as _chmod

    @functools.wraps(_chmod)
    def chmod(path, *args, **kw):  # pylint: disable=missing-docstring
        if isinstance(path, Path):
            path = str(path)
        return _chmod(path, *args, **kw)

else:
    from os import chmod
    open = open  # pylint: disable=invalid-name,self-assigning-variable


__all__ = ('chmod', 'open')

# -*- coding: utf-8 -*-
#
# Copyright 2018  Ternaris.
# SPDX-License-Identifier: Apache-2.0

"""Load configuration from environment variables."""

import os
from collections import namedtuple
from pathlib import Path

from .registry import Image
from .utils import find_file


Config = namedtuple('Config', '''
broken_docker_exec
debug
disable_nvidia_docker
home
images
name
gitlab
registry
docker_run_args
''')


def load_config():
    """Load configuration from environment variables."""
    home = os.environ.get('ADE_HOME', find_file('.adehome', parent=True))
    cfg = Config(**{
        'broken_docker_exec': bool(os.environ.get('ADE_BROKEN_DOCKER_EXEC')),
        'debug': os.environ.get('ADE_DEBUG'),
        'disable_nvidia_docker': bool(os.environ.get('ADE_DISABLE_NVIDIA_DOCKER')),
        'home': Path(home) if home else None,
        'images': [Image(x) for x in os.environ.get('ADE_IMAGES', '').split()],
        'name': os.environ.get('ADE_NAME', 'ade'),
        'gitlab': os.environ.get('ADE_GITLAB'),
        'registry': os.environ.get('ADE_REGISTRY'),
        'docker_run_args': tuple(os.environ.get('ADE_DOCKER_RUN_ARGS', '').split()),
    })
    return cfg

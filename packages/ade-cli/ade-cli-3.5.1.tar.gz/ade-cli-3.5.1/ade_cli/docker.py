# -*- coding: utf-8 -*-
#
# Copyright 2017 - 2018  Ternaris.
# SPDX-License-Identifier: Apache-2.0

"""Manage docker images and containers."""

import json
import os
import sys
from subprocess import CalledProcessError, DEVNULL, PIPE, Popen

from ade_cli import __version__ as VERSION
from .registry import Image, login, pull_if_missing, update_image
from .utils import get_timezone
from .utils import run, runout, shell, shellout


DEBUG = False


def docker_exec(name, cmd=None, user=None, broken=False):
    """Enter container or run command inside container."""
    if not user:
        user = shellout('id -un').strip()

    if broken:
        # Workaround for broken docker exec on arm64
        # https://github.com/docker/for-linux/issues/105#issuecomment-429404607
        pid = runout(['docker', 'inspect', '--format', '{{.State.Pid}}', name]).strip()
        args = [
            'sudo', 'nsenter', '--target', pid, '--mount', '--uts', '--ipc', '--pid',
            '/usr/sbin/chroot', '/new_root',
            '/usr/bin/sudo', '-Hu', user, '--',
            'bash', '-li'
        ]
    else:
        args = [
            'docker', 'exec', '-ti',
            '--env', 'COLORFGBG',
            '--env', 'TERM',
            '-u', user,
            name,
            'bash', '-li',
        ]

    if cmd:
        args.extend(['-c', cmd])

    print('Entering {} with following images:'.format(name))
    print_image_matrix(name)
    run(args, check='exit')


def docker_run(name, image, home, addargs=None, debug=None, volume_images=None,
               disable_nvidia_docker=False):
    """Create and start main and volume containers."""
    # pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements

    user = shellout('id -un').strip()
    user_id = int(shellout('id -u').strip())
    group = shellout('id -gn').strip()
    group_id = int(shellout('id -g').strip())
    video_group_id = int(shellout('getent group video |cut -d: -f3').strip())

    cmd = [
        'docker', 'run',
        '-h', name,
        '--detach',
        '--name', name,
        '--env', 'COLORFGBG',
        '--env', 'DISPLAY',
        '--env', 'EMAIL',
        '--env', 'GIT_AUTHOR_EMAIL',
        '--env', 'GIT_AUTHOR_NAME',
        '--env', 'GIT_COMMITTER_EMAIL',
        '--env', 'GIT_COMMITTER_NAME',
        '--env', 'SSH_AUTH_SOCK',
        '--env', 'TERM',
        '--env', 'TIMEZONE={}'.format(get_timezone()),
        '--env', 'USER={}'.format(user),
        '--env', 'GROUP={}'.format(group),
        '--env', 'USER_ID={}'.format(user_id),
        '--env', 'GROUP_ID={}'.format(group_id),
        '--env', 'VIDEO_GROUP_ID={}'.format(video_group_id),
        '-v', '/dev/dri:/dev/dri',
        '-v', '/dev/shm:/dev/shm',
        '-v', '/tmp/.X11-unix:/tmp/.X11-unix',
        '-v', '{}:/home/{}'.format(home.resolve(), user),
        '--env', 'ADE_CLI_VERSION={}'.format(VERSION),
        '--env', 'ADE_HOME_HOSTPATH={}'.format(home.resolve()),
        '--label', 'ade_version={}'.format(VERSION),
    ]

    dotssh = home / '.ssh'
    try:
        os.mkdir(str(dotssh))
    except FileExistsError:
        pass
    else:
        (dotssh / 'WILL_BE_MOUNTED_FROM_OUTSIDE').write_text('')
    cmd.extend(['-v', '{}/.ssh:/home/{}/.ssh'.format(os.environ['HOME'], user)])

    if os.environ.get('SSH_AUTH_SOCK'):
        cmd.extend(['-v', '{x}:{x}'.format(x=os.environ.get('SSH_AUTH_SOCK'))])

    if debug:
        cmd.extend(['--env', 'DEBUG=1'])

    volumes_from = []
    for img in volume_images or ():
        container = make_container(envname=name, image=img)
        cmd.extend(['--volumes-from', '{}:ro'.format(container)])
        volumes_from.append(container)
    cmd.extend(['--label', 'ade_volumes_from={}'.format(json.dumps(volumes_from))])

    if os.path.exists('/dev/nvidia0') and not disable_nvidia_docker:
        try:
            nvidia_docker_args = shellout('curl -s http://localhost:3476/docker/cli').split()
            print("WARNING. nvidia-docker1 has been deprecated. "
                  "Please install nvidia-docker2 instead. "
                  "https://github.com/NVIDIA/nvidia-docker", file=sys.stderr)
        except CalledProcessError:
            nvidia_docker_args = ["--runtime=nvidia",
                                  "--env", "NVIDIA_VISIBLE_DEVICES=all",
                                  "--env", "NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics"]

        cmd.extend(nvidia_docker_args)
        cmd.extend(['--env', 'LD_LIBRARY_PATH=/usr/local/nvidia/lib64'])

    if addargs:
        cmd.extend(addargs)

    pull_if_missing(image)

    image_info = []
    for img in [image] + list(volume_images or ()):
        commit_sha = get_label(img.fqn, 'ade_image_commit_sha', default='')
        commit_tag = get_label(img.fqn, 'ade_image_commit_tag', default='')
        safename = img.name.upper().replace('-', '_')
        cmd.extend(['--env', 'ADE_IMAGE_{}_FQN={}'.format(safename, img.fqn)])
        cmd.extend(['--env', 'ADE_IMAGE_{}_COMMIT_SHA={}'.format(safename, commit_sha)])
        cmd.extend(['--env', 'ADE_IMAGE_{}_COMMIT_TAG={}'.format(safename, commit_tag)])
        image_info.append({
            'fqn': img.fqn,
            'commit_sha': commit_sha,
            'commit_tag': commit_tag,
        })
    cmd.extend(['--label', 'ade_images={}'.format(json.dumps(image_info))])

    cmd.append(image.fqn)
    did = runout(cmd, check=DEBUG or 'exit').strip()

    if os.environ.get('DISPLAY'):
        host = runout(['docker', 'inspect', "--format='{{ .Config.Hostname }}'", did],
                      check=DEBUG or 'exit')
        cp = shell("xhost +local:{}".format(host), check=False)
        if cp.returncode != 0:
            print("WARNING: Could not find xhost, you won't be able to launch X applications")

    logtail = Popen(['docker', 'logs', '-f', name], stdout=PIPE)
    line = None
    while line != 'ADE startup completed.':
        line = logtail.stdout.readline().decode('utf-8')
        if not line:
            break
        line = line.rstrip()
        print(line)
    else:
        return True
    return False


def docker_stop(name):
    """Stop main and volume containers."""
    containers = [x for x in shellout("docker ps --format '{{.Names}}'").split()
                  if x == name or x.startswith('{}_'.format(name))]
    for container in containers:
        print('Stopping', container)
        run(['docker', 'stop', '-t', '0', container], stdout=DEVNULL, stderr=DEVNULL, check=False)


def get_label(name, key, default=None, dejson=False):
    """Get label for key from specific container."""
    try:
        out = runout(['docker', 'inspect', '--format', '{{json .Config.Labels}}', name])
    except CalledProcessError:
        return default

    labels = json.loads(out)
    try:
        value = labels[key]
    except (KeyError, TypeError):
        return default

    if dejson:
        return json.loads(value)
    return value


def is_running(name):
    """Check if specific container is running"""
    return name in shellout("docker ps --format '{{.Names}}'").split()


def make_container(envname, image, recreate=None):
    """Create container for image."""
    fqn = image.fqn
    name = '{}_{}'.format(envname, fqn.replace('/', '_').replace(':', '_'))

    if recreate:
        run(['docker', 'rm', '--force', '--volumes', name],
            check=False, stdout=DEVNULL, stderr=DEVNULL)
        existing = ()
    else:
        existing = shellout("docker ps -a --format '{{.Names}}'").split()

    if name not in existing:
        print('Creating volume container for', fqn)
        cmd = ['docker', 'run', '--label', 'ade_version={}'.format(VERSION),
               '--read-only', '--detach', '--name', name, fqn]
        try:
            run(cmd, stdout=DEVNULL, stderr=DEVNULL)
        except CalledProcessError:
            login(image)
            run(cmd, stdout=DEVNULL, check=DEBUG or 'exit')
    else:
        run(['docker', 'start', name], check=DEBUG or 'exit')

    return name


def print_image_matrix(name, images=None):
    """Print images used by container."""
    images = images or [Image(x['fqn']) for x in get_label(name, 'ade_images', dejson=True)]
    matrix = []
    for img in images:
        commit_sha = get_label(img.fqn, 'ade_image_commit_sha', default='n/a')
        commit_tag = get_label(img.fqn, 'ade_image_commit_tag')
        matrix.append((img.name, commit_tag or commit_sha[:12], img.tag, img.fqn))
    aligns = [max([(len(x) or 1)for x in col]) for col in zip(*matrix)]
    for line in matrix:
        fmt = ' | '.join(['{:%s}' % x for x in aligns])
        print(fmt.format(*line))


async def update_images(envname, images):
    """Update docker images from registry and recreate containers."""
    for img in images:
        try:
            if await update_image(img):
                make_container(envname=envname, image=img, recreate=True)
        except CalledProcessError as e:
            print(str(e), file=sys.stderr)
            sys.exit(e.returncode)

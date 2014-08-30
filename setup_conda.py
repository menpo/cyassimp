#!/usr/bin/env python
import subprocess
import os.path as p
from functools import partial

yaml_version_placeholder = 'VERSION_NUMBER'

# forward stderr to stdout
co = partial(subprocess.check_output, stderr=subprocess.STDOUT)


def execute(cmd, verbose=False):
    if verbose:
        print('> {}'.format(' '.join(cmd)))
    result = co(cmd)
    if verbose:
        print(result)
    return result

# eXecute and display status
x = partial(execute, verbose=True)

miniconda_dir = p.expanduser('~/miniconda')

# define our commands
mc_bin_dir = p.join(miniconda_dir, 'bin')
conda = p.join(mc_bin_dir, 'conda')
conda_build = p.join(mc_bin_dir, 'conda-build')
binstar = p.join(mc_bin_dir, 'binstar')


def run_commands(*cmds):
    try:
        for cmd in cmds:
            x(cmd)
    except subprocess.CalledProcessError as e:
        print(' -> {}'.format(e.output))
        raise e


def setup_conda(url, channel=None):
    miniconda_file = 'miniconda.sh'
    cmds =[['wget', '-nv', url, '-O', miniconda_file],
           ['chmod', '+x', miniconda_file],
           [p.join('.', miniconda_file), '-b', '-p', miniconda_dir],
           [conda, 'update', '--yes', 'conda'],
           [conda, 'install', '--yes', 'conda-build', 'jinja2', 'binstar']]
    if channel is not None:
        cmds.append([conda, 'config', '--add', 'channels', channel])
    run_commands(*cmds)


def get_version():
    raw_describe = x(['git', 'describe', '--tag'])
    # conda does not like '-' in version strings
    return raw_describe.strip().replace('-', '_')[1:]


def replace_text_in_file(path, placeholder, replacement):
    with open(path, 'rb') as f:
        meta = f.read()
    with open(path, 'wb') as f:
        f.write(meta.replace(placeholder, replacement))


def build(path):
    x([conda, 'build', path])


def get_conda_build_path(path):
    from conda_build.metadata import MetaData
    from conda_build.build import bldpkg_path
    return bldpkg_path(MetaData(path))


def upload_to_binstar(key, user, channel, path):
    run_commands([binstar, '-t', key, 'upload', '-u', user, '-c', channel, path])


def build_and_upload(path, key, user, channel):
    build(path)
    # get a handle on the conda output
    built_tar = get_conda_build_path(path)
    upload_to_binstar(key, user, channel, built_tar)


def setup_and_find_version(url, build_dir, channel=None):
    setup_conda(url, channel='menpo')

    # update the yaml file to have the verion number
    replace_text_in_file(p.join(build_dir, 'meta.yaml'), yaml_version_placeholder, get_version())

import os
# grab the URL
url = os.environ.get('MINICONDA_URL')

# STAGE 1

#setup_and_find_version(url, os.getcwd(), channel='menpo')

# STAGE 2

# # grab the binstar key
# key = os.environ.get('BINSTAR_KEY')

# build_and_upload(os.getcwd(), key, 'menpo', 'testing')

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description=r"""
        Setup conda, version meta.yaml, and upload to binstar on Travis CI.
        """)
    parser.add_argument("mode", help="'setup' or 'build'")
    parser.add_argument("path", help="path to the conda build scripts")
    parser.add_argument("-u", "--url", help="URL to download miniconda from")
    parser.add_argument("-k", "--key", help="The binstar key for uploading")
    ns = parser.parse_args()

    if ns.mode == 'setup':
        url = ns.url
        if url is None:
            raise ValueError("You must provide a miniconda URL for the setup command")
        setup_and_find_version(url, ns.path, channel='menpo')
    elif ns.mode == 'build':
        key = ns.key
        if key is None:
            raise ValueError("You must provide a key for the build script.")
        build_and_upload(ns.path, key, 'menpo', 'testing')

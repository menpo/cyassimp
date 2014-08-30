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


def run_commands(*cmds, **kwargs):
    verbose = kwargs.get('verbose', True)
    try:
        for cmd in cmds:
            execute(cmd, verbose)
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
    # verbose false as we don't want to print our key to Travis!
    run_commands([binstar, '-t', key, 'upload', '-u', user, '-c', channel,
                  path], verbose=True)


def upload(path, key, user, channel):
    # get a handle on the conda output
    built_tar = get_conda_build_path(path)
    upload_to_binstar(key, user, channel, built_tar)


def setup_and_find_version(url, build_dir, channel=None):
    setup_conda(url, channel=channel)

    # update the yaml file to have the verion number
    replace_text_in_file(p.join(build_dir, 'meta.yaml'), yaml_version_placeholder, get_version())

import os
# grab the URL
url = os.environ.get('MINICONDA_URL')


def resolve_if_can_upload_from_travis():
    pr = os.environ['TRAVIS_PULL_REQUEST']
    print("Deciding if we can upload")
    print(pr)
    # not on a PR -> can upload
    return pr is None


def resolve_channel_from_travis_state():
    branch = os.environ['TRAVIS_BRANCH']
    tag = os.environ['TRAVIS_TAG']
    if tag is not None and branch == 'master':
        # final release, channel is 'main'
        print("on a tag and on branch master -> upload to 'main'")
        return 'main'
    else:
        print("not on a tag on master - just upload to the branch name {"
              "}".format(branch))
        return branch


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description=r"""
        Setup conda, version meta.yaml, and upload to binstar on Travis CI.
        """)
    parser.add_argument("mode", choices=['setup', 'build'])
    parser.add_argument("path", help="path to the conda build scripts")
    parser.add_argument("--url", help="URL to download miniconda from")
    parser.add_argument("-c", "--channel", help="binstar channel to activate "
                                                "(setup only)")
    parser.add_argument("-u", "--user", help="binstar user to upload to "
                                             "(build only)")
    parser.add_argument("-k", "--key", help="The binstar key for uploading")
    ns = parser.parse_args()

    if ns.mode == 'setup':
        url = ns.url
        if url is None:
            raise ValueError("You must provide a miniconda URL for the setup command")
        setup_and_find_version(url, ns.path, channel=ns.channel)
    elif ns.mode == 'build':
        print('Going into build mode')
        key = ns.key
        if key is None:
            raise ValueError("You must provide a key for the build script.")
        print('building using path: {}'.format(ns.path))
        build(ns.path)
        can_upload = resolve_if_can_upload_from_travis()
        if can_upload:
            channel = resolve_channel_from_travis_state()
            upload(ns.path, key, ns.user, 'testing')

#!/usr/bin/env python
import subprocess
import os.path as p
from functools import partial

co = partial(subprocess.check_output, stderr=subprocess.STDOUT)


def x(cmd):
    print('> {}'.format(' '.join(cmd)))
    print(co(cmd))


# define filenames
miniconda_file = 'miniconda.sh'
miniconda_dir = p.expanduser('~/miniconda')

# define our commands
mc_bin_dir = p.join(miniconda_dir, 'bin')
conda = p.join(mc_bin_dir, 'conda')
conda_build = p.join(mc_bin_dir, 'conda-build')
binstar = p.join(mc_bin_dir, 'binstar')

import os
# grab the URL
url = os.environ.get('MINICONDA_URL')

try:
    x(['wget', url, '-O', miniconda_file])
    x(['chmod', '+x', miniconda_file])
    x([p.join('.', miniconda_file), '-b', '-p', miniconda_dir])
    x([conda, 'update', '--yes', 'conda'])
    x([conda, 'install', '--yes', 'conda-build', 'jinja2', 'binstar'])
    x([conda, 'config', '--add', 'channels', 'menpo'])
except subprocess.CalledProcessError as e:
    print(' -> {}'.format(e.output))

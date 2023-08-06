#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# (c) Copyright 2018 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from __future__ import print_function

import distutils.spawn
import os
from contextlib import contextmanager
import subprocess
import re

from nose import SkipTest

try:
    from unittest import mock
except ImportError:
    import mock

try:
    from tempfile import TemporaryDirectory
except ImportError:
    from backports.tempfile import TemporaryDirectory


@contextmanager
def reroot_cvm(root):
    from LbPlatformUtils import inspect
    try:
        bkup = inspect.SINGULARITY_ROOTS
        inspect.SINGULARITY_ROOTS = [
            (os.path.join(root, os.path.basename(path)), os_id)
            for path, os_id in inspect.SINGULARITY_ROOTS
        ]
        yield
    finally:
        inspect.SINGULARITY_ROOTS = bkup


def test_singularity_fake():
    from LbPlatformUtils import inspect
    with TemporaryDirectory() as temp_dir:
        os.environ['PATH'] = temp_dir + os.pathsep + os.environ['PATH']
        with open(os.path.join(temp_dir, 'singularity'), 'wb') as script:
            script.writelines([b'#!/bin/sh\n',
                               b'echo ${TEST_SING_OUTPUT:-${PWD}}\n',
                               b'exit ${TEST_SING_EXIT:-0}\n'])
        os.chmod(os.path.join(temp_dir, 'singularity'), 0o775)
        os.mkdir(os.path.join(temp_dir, 'cvm4'))
        os.mkdir(os.path.join(temp_dir, 'cvm3'))
        with reroot_cvm(temp_dir):
            # test no singularity
            os.environ['TEST_SING_EXIT'] = '1'
            assert inspect.singularity_os_ids() == []

            del os.environ['TEST_SING_EXIT']
            assert inspect.singularity_os_ids() == inspect.SINGULARITY_ROOTS

            from LbPlatformUtils import get_viable_containers
            from LbPlatformUtils.describe import platform_info
            assert 'singularity' in get_viable_containers(
                platform_info(), 'x86_64-slc6-gcc49-opt')

            from LbPlatformUtils import dirac_platform
            from LbPlatformUtils.inspect import architecture
            arch = architecture()
            assert '-'.join([arch, 'any']) != dirac_platform()
            assert '-'.join([arch, 'any']) != dirac_platform(allow_containers=False)
            assert '-'.join([arch, 'any']) == dirac_platform(allow_containers=True)

            os.environ['TEST_SING_OUTPUT'] = '/some/other/directory'
            assert inspect.singularity_os_ids() == []
            del os.environ['TEST_SING_OUTPUT']


def test_singularity_real():
    from LbPlatformUtils import inspect

    if not os.path.isdir('/cvmfs/cernvm-prod.cern.ch'):
        raise SkipTest("Skipping test_singularity_real due to missing cernvm")
    if not distutils.spawn.find_executable('singularity'):
        raise SkipTest("Skipping test_singularity_real due to missing singularity")

    # Only singularity 3 will work correctly
    singularity_version = subprocess.check_output(['singularity', '--version']).decode()
    match = re.search(r'(?:^| )(\d+)\.\d+\.\d+', singularity_version)
    assert match, singularity_version
    if int(match.groups()[0]) >= 3:
        expected_result = inspect.SINGULARITY_ROOTS
    else:
        expected_result = []

    assert inspect.singularity_os_ids() == expected_result

# Copyright (c) 2019 Intel Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Module for installation packages of components from manifest file
"""

import logging
from common.manifest_manager import Manifest, get_build_dir
from common import package_manager
from common.system_info import get_pkg_type


def install_components(manifest, components):
    """
    :param manifest: Path to a manifest file
    :type manifest: String | Manifest

    :param components: List of components to install
    :type components: List

    :return: Boolean
    """

    if not isinstance(manifest, Manifest):
        manifest = Manifest(manifest)

    pkg_type = get_pkg_type()
    log = logging.getLogger('install_components')

    for component in components:
        log.info(f'Installing component: {component}')
        comp = manifest.get_component(component)
        if not comp:
            log.error(f'{component} does not exist in manifest')
            return False

        artifacts = get_build_dir(manifest, component)
        packages = [pkg_path for pkg_path in artifacts.glob(f'*.{pkg_type}')
                    if component in pkg_path.name.lower()]

        # TODO: solve situation with multiple packages installation, e.g. "package" and "package-devel"
        if not packages:
            log.info(f'Package "{component}" was not found in {artifacts}')
            return False
        elif len(packages) > 1:
            log.info(f'Found multiple "{component}" packages {packages} in {artifacts}')
            return False

        if not package_manager.uninstall_pkg(component):
            return False

        if not package_manager.install_pkg(packages[0]):
            return False

    return True

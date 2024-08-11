# Get custom libraries
# Downloads to PC, so needed for each machine
# Tobiloba Kujore

from typing import List

import pip
from pkg_resources import working_set

def _get_current_packages():
    return [x.project_name for x in working_set]

def _install_package(package_name: str):
    pip.main(['install', package_name,])

def import_packages(dependencies: List[str]):
    currently_installed = _get_current_packages()

    for dependency in dependencies:
        if dependency in currently_installed:
            continue

        _install_package(dependency)
        currently_installed.append(dependency)



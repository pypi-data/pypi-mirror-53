"""Version and diagnostic information for the mudpy engine."""

# Copyright (c) 2018 mudpy authors. Permission to use, copy,
# modify, and distribute this software is granted under terms
# provided in the LICENSE file distributed with this software.

import json
import pkg_resources
import sys


class VersionDetail:

    """Version detail for a Python package."""

    def __init__(self, package):
        self.project_name = _normalize_project(package.project_name)
        version = package.version
        self.version_info = tuple(version.split('.'))

        # Build up a human-friendly version string for display purposes
        self.text = "%s %s" % (self.project_name, version)

        # Obtain Git commit ID from PBR metadata if present
        dist = pkg_resources.get_distribution(self.project_name)
        try:
            self.git_version = json.loads(
                dist.get_metadata("pbr.json"))["git_version"]
            self.text = "%s (%s)" % (self.text, self.git_version)
        except (IOError, KeyError):
            self.git_version = None

    def __repr__(self):
        return self.text


class Versions:

    """Tracks info on known Python package versions."""

    def __init__(self, project_name):
        # Normalize the supplied name
        project_name = _normalize_project(project_name)

        # Python info for convenience
        self.python_version = "%s Python %s" % (
            sys.platform, sys.version.split(" ")[0])

        # List of package names for this package's declared dependencies
        requirements = []
        for package in pkg_resources.get_distribution(project_name).requires():
            requirements.append(_normalize_project(package.project_name))

        # Accumulators for Python package versions
        self.dependencies = {}
        self.environment = {}

        # Loop over all installed packages
        for package in pkg_resources.working_set:
            version = VersionDetail(package)
            # Sort packages into the corresponding buckets
            if version.project_name in requirements:
                # This is a dependency
                self.dependencies[version.project_name] = version
            elif version.project_name == project_name:
                # This is our main package
                self.version = version
            else:
                # This may be a transitive dep, or merely installed
                self.environment[version.project_name] = version

        self.dependencies_text = ", ".join(
            sorted([x.text for x in self.dependencies.values()]))
        self.environment_text = ", ".join(
            sorted([x.text for x in self.environment.values()]))

    def __repr__(self):
        return "Running %s on %s with dependencies %s." % (
            self.version.text,
            self.python_version,
            self.dependencies_text,
            )


def _normalize_project(project_name):
    """Convenience function to normalize Python project names."""
    return pkg_resources.safe_name(project_name).lower()

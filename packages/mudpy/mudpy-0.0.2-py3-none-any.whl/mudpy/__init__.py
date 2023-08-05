"""Core modules package for the mudpy engine."""

# Copyright (c) 2004-2018 mudpy authors. Permission to use, copy,
# modify, and distribute this software is granted under terms
# provided in the LICENSE file distributed with this software.

import importlib  # noqa (referenced via exec of string literal below)

import mudpy  # noqa (referenced via exec of string literal below)


def load():
    """Import/reload some modules (be careful, as this can result in loops)."""

    # pick up the modules list from this package
    global modules

    # iterate over the list of modules provided
    for module in modules:

        # attempt to reload the module, assuming it was probably imported
        # earlier
        try:
            exec("importlib.reload(%s)" % module)

        # must not have been, so import it now
        except NameError:
            exec("import mudpy.%s" % module)


# load the modules contained in this package
modules = ["command", "data", "misc", "password", "telnet", "version"]
load()

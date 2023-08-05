=============
 coder guide
=============

.. Copyright (c) 2004-2019 mudpy authors. Permission to use, copy,
   modify, and distribute this software is granted under terms
   provided in the LICENSE file distributed with this software.

This guide attempts to embody a rudimentary set of rules for developer
submissions of source code and documentation targeted for inclusion
within the mudpy project, as well as pointers to useful resources for
those attempting to obtain a greater understanding of the software.

source
------

As with any project, the mudpy source code could always be better
documented, and contributions to that end are heartily welcomed.

version control system
~~~~~~~~~~~~~~~~~~~~~~

Git_ is used for version control on the project, and the archive can
be browsed or cloned anonymously from https://mudpy.org/code/mudpy .
For now, detailed commits can be E-mailed to fungi@yuggoth.org, but
there will most likely be a developer mailing list for more open
presentation and discussion of patches soon.

A :file:`ChangeLog` is generated automatically from repository
commit logs, and is included automatically in all sdist_ tarballs. It
can be regenerated easily by running :command:`tox -e dist` from the
top level directory of the Git repository in a working `developer
environment`_.

.. _Git: https://git-scm.com/
.. _sdist: https://packaging.python.org/glossary
           /#term-source-distribution-or-sdist

developer environment
~~~~~~~~~~~~~~~~~~~~~

Basic developer requirements are a POSIX Unix derivative (such as
Linux), a modern Python 3 interpreter (any of the minor revisions
mentioned in the ``metadata.classifier`` section of
:file:`setup.cfg`) and a recent release of the tox_ utility (at least
the ``tox.minversion`` mentioned in :file:`tox.ini`). The tox-venv_
plug-in for tox is also recommended.

.. _tox: https://tox.readthedocs.io/
.. _tox-venv: https://pypi.org/project/tox-venv/

application program interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :doc:`api` API documentation is maintained within docstrings in
the mudpy source code.

regression testing
~~~~~~~~~~~~~~~~~~

All new commits are tested using a selftest script in the
``mudpy/tests`` directory of the source archive, to help ensure the
software is continually usable. Any new features should be
accompanied by suitable regression tests so that their functionality
can be maintained properly through future releases. The selftest can
be invoked with ``tox -e selftest`` after starting the daemon with
the test configuration provided in the ``mudpy/tests/fixtures``
directory.

style
-----

This project follows Guido van Rossum and Barry Warsaw's `Style Guide`_
for Python Code (a.k.a. "PEP-8"). When in need of sample code or other
examples, any common source code file or text document file distributed
as part of mudpy should serve as a suitable reference. Testing of all
new patches with the flake8_ utility should be performed with ``tox
-e flake8`` to ensure adherence to preferred style conventions.

.. _Style Guide: :pep:`0008`
.. _flake8: https://pypi.org/project/flake8

test and demo walk-through
--------------------------

The included tox configuration provides testenv definitions for a
variety of analyzers, regression tests, documentation builds and
package generation. It also has a ``demo`` testenv which will run the
server using the provided :file:`etc/mudpy.yaml` and other sample
files. By default it listens on TCP port 4000 at the IPv6 loopback
address, streams its logging to the terminal via stdout, and grants
administrative rights automatically to an account named ``admin``
(once created).

Because all the dependencies besides the ``python3`` interpreter itself
are available from PyPI, installing them should be fairly similar
across most GNU/Linux distributions. For example, on Debian 10 (a.k.a.
"Buster") you need to expressly install the ``pip`` and ``venv`` modules
since they're packaged separately from the rest of the Python standard
library. Once that's done, you can perform local installs of ``tox`` and
``tox-venv`` as a normal non-root user. We're also going to install
system packages for the ``git`` revision control toolset and an
extensible console-based MUD client called ``tf5`` (TinyFugue version
5)::

    sudo apt install git python3-pip python3-venv tf5
    pip install --user tox tox-venv
    exit

The reason for exiting is that, if this is the first time you've ever
used pip's ``--user`` option, when you log back in your ``~/.profile``
should see that there's now a ``~/.local/bin`` directory and add it to
your ``$PATH`` environment variable automatically from that point on.
Next, retrieve the project source code and switch your current working
directory to where you've cloned it::

    git clone https://mudpy.org/code/mudpy
    cd mudpy

Now you should be able to invoke any tox testenv you like. Just
running ``tox`` without any additional options will go through the
defalt battery of checks and is a good way to make sure everything is
installed and working. Once you're ready to try out the server
interactively, launch it like this::

    tox -e demo

Now in another terminal/session (because the one you've been using is
busy displaying the server's logs) connect using a MUD client::

    tf5 ip6-localhost 4000

Log in as ``admin`` creating an account and then an avatar and awaken
it. Try out the ``help`` command and make sure you see some command
words in red (you're using a color terminal, right?) since those are
admin-only commands and being able to see them confirms you're an
administrator. When you're ready to terminate the service you can
either give the ``halt`` command in your MUD client terminal or press
the ``control`` and ``c`` keys together in the terminal where you ran
tox. To exit the MUD client, give it the ``/quit`` command.

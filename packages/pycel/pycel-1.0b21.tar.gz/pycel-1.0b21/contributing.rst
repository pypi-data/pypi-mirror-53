
Clean up documentation for public API
sphinx
Document the Plugin system (This is part of Excel Compiler)

Contributing Outline:

Say thanks and define what is contributing
Issues and Feature Requests
Pull Request Mechanics
  tox  (find a how to)
  travis  (find a how to hookup)
  code coverage  (find a how to hookup)



An excerpt from the Travis Tutorial`_ on how to setup Travis CI

#. Go to `Travis-ci.com`_ and `Sign up with GitHub`_.

#. Accept the Authorization of Travis CI. You’ll be redirected to
   GitHub.

#. Click the green *Activate* button, and select the repositories you
   want to use with Travis CI.

#. Next time you push a change to github, it should trigger a
   Travis CI build.

#. Check the build status page to see if your build `passes or fails`_,
   according to the return status of the build command by visiting the
   `Travis CI`_ and selecting your repository.

.. _Travis Tutorial: https://docs.travis-ci.com/user/tutorial/
.. _Travis-ci.com: https://travis-ci.com
.. _Sign up with GitHub: https://travis-ci.com/signin
.. _passes or fails: https://docs.travis-ci.com/user/job-lifecycle/#breaking-the-build
.. _Travis CI: https://travis-ci.com/auth


####################################################


Django:

Be rigorous

When we say “PEP 8, and must have docs and tests”, we mean it. If a patch doesn’t have docs and tests, there had better be a good reason. Arguments like “I couldn’t find any existing tests of this feature” don’t carry much weight–while it may be true, that means you have the extra-important job of writing the very first tests for that feature, not that you get a pass from writing tests altogether.



################### FLASK ########################

How to contribute to Pycel
==========================

Thank you for considering contributing to Pycel!

Support questions
-----------------

Please, don't use the issue tracker for this. Use one of the following
resources for questions about your own code:

* Ask on `Stack Overflow`_. Search with Google first using:
  ``site:stackoverflow.com flask {search term, exception message, etc.}``

.. _Stack Overflow: https://stackoverflow.com/questions/tagged/flask?sort=linked

Reporting issues
----------------

- Describe what you expected to happen.
- If possible, include a `minimal, complete, and verifiable example`_ to help
  us identify the issue. This also helps check that the issue is not with your
  own code.
- Describe what actually happened. Include the full traceback if there was an
  exception.
- List your Python and Pycel versions. If possible, check if this
  issue is already fixed in the repository.

.. _minimal, complete, and verifiable example: https://stackoverflow.com/help/mcve

Submitting patches
------------------

- Include tests if your patch is supposed to solve a bug, and explain
  clearly under which circumstances the bug happens. Make sure the test fails
  without your patch.
- The tests use flake8 and will fail if certain aspects of `PEP8`_ are not
  followed.

First time setup
~~~~~~~~~~~~~~~~

- Download and install the `latest version of git`_.
- Configure git with your `username`_ and `email`_::

        git config --global user.name 'your name'
        git config --global user.email 'your email'

- Make sure you have a `GitHub account`_.
- Fork Pycel to your GitHub account by clicking the `Fork`_ button.
- `Clone`_ your GitHub fork locally::

        git clone https://github.com/{username}/pycel
        cd flask

- Add the main repository as a remote to update later::

        git remote add pycel https://github.com/dgorissen/pycel
        git fetch pycel

- Create a virtualenv::

        python3 -m venv venv
        . venv/bin/activate
        # or "venv\Scripts\activate" on Windows

- Install Flask in editable mode with development dependencies::

        pip install -e ".[dev]"

.. _GitHub account: https://github.com/join
.. _latest version of git: https://git-scm.com/downloads
.. _username: https://help.github.com/articles/setting-your-username-in-git/
.. _email: https://help.github.com/articles/setting-your-email-in-git/
.. _Fork: https://github.com/pallets/flask/fork
.. _Clone: https://help.github.com/articles/fork-a-repo/#step-2-create-a-local-clone-of-your-fork

Start coding
~~~~~~~~~~~~

- Create a branch to identify the issue you would like to work on (e.g.
  ``2287-dry-test-suite``)
- Using your favorite editor, make your changes, `committing as you go`_.
- Try to follow `PEP8`_, but you may ignore the line length limit if following
  it would make the code uglier.
- Include tests that cover any code changes you make. Make sure the test fails
  without your patch. `Run the tests. <contributing-testsuite_>`_.
- Push your commits to GitHub and `create a pull request`_.
- Celebrate 🎉

.. _committing as you go: https://dont-be-afraid-to-commit.readthedocs.io/en/latest/git/commandlinegit.html#commit-your-changes
.. _PEP8: https://pep8.org/
.. _create a pull request: https://help.github.com/articles/creating-a-pull-request/

.. _contributing-testsuite:

Running the tests
~~~~~~~~~~~~~~~~~

Run the basic test suite with::

    pytest

This only runs the tests for the current environment. Whether this is relevant
depends on which part of Flask you're working on. Travis-CI will run the full
suite when you submit your pull request.

The full test suite takes a long time to run because it tests multiple
combinations of Python and dependencies. You need to have Python 2.7, 3.4,
3.5 3.6, and PyPy 2.7 installed to run all of the environments. Then run::

    tox

Running test coverage
~~~~~~~~~~~~~~~~~~~~~

Generating a report of lines that do not have test coverage can indicate
where to start contributing. Run ``pytest`` using ``coverage`` and generate a
report on the terminal and as an interactive HTML document::

    coverage run -m pytest
    coverage report
    coverage html
    # then open htmlcov/index.html

Read more about `coverage <https://coverage.readthedocs.io>`_.

Running the full test suite with ``tox`` will combine the coverage reports
from all runs.


Building the docs
~~~~~~~~~~~~~~~~~

Build the docs in the ``docs`` directory using Sphinx::

    cd docs
    make html

Open ``_build/html/index.html`` in your browser to view the docs.

Read more about `Sphinx <https://www.sphinx-doc.org>`_.


make targets
~~~~~~~~~~~~

Flask provides a ``Makefile`` with various shortcuts. They will ensure that
all dependencies are installed.

- ``make test`` runs the basic test suite with ``pytest``
- ``make cov`` runs the basic test suite with ``coverage``
- ``make test-all`` runs the full test suite with ``tox``
- ``make docs`` builds the HTML documentation

Caution: zero-padded file modes
-------------------------------

This repository contains several zero-padded file modes that may cause issues
when pushing this repository to git hosts other than GitHub. Fixing this is
destructive to the commit history, so we suggest ignoring these warnings. If it
fails to push and you're using a self-hosted git service like GitLab, you can
turn off repository checks in the admin panel.

These files can also cause issues while cloning. If you have ::

    [fetch]
    fsckobjects = true

or ::

    [receive]
    fsckObjects = true

set in your git configuration file, cloning this repository will fail. The only
solution is to set both of the above settings to false while cloning, and then
setting them back to true after the cloning is finished.










################## REQUESTS ####################





# Contribution Guidelines

Before opening any issues or proposing any pull requests, please do the
following:

1. Read our [Contributor's Guide](http://docs.python-requests.org/en/latest/dev/contributing/).
2. Understand our [development philosophy](http://docs.python-requests.org/en/latest/dev/philosophy/).

To get the greatest chance of helpful responses, please also observe the
following additional notes.

## Questions

The GitHub issue tracker is for *bug reports* and *feature requests*. Please do
not use it to ask questions about how to use Requests. These questions should
instead be directed to [Stack Overflow](https://stackoverflow.com/). Make sure
that your question is tagged with the `python-requests` tag when asking it on
Stack Overflow, to ensure that it is answered promptly and accurately.

## Good Bug Reports

Please be aware of the following things when filing bug reports:

1. Avoid raising duplicate issues. *Please* use the GitHub issue search feature
   to check whether your bug report or feature request has been mentioned in
   the past. Duplicate bug reports and feature requests are a huge maintenance
   burden on the limited resources of the project. If it is clear from your
   report that you would have struggled to find the original, that's ok, but
   if searching for a selection of words in your issue title would have found
   the duplicate then the issue will likely be closed extremely abruptly.
2. When filing bug reports about exceptions or tracebacks, please include the
   *complete* traceback. Partial tracebacks, or just the exception text, are
   not helpful. Issues that do not contain complete tracebacks may be closed
   without warning.
3. Make sure you provide a suitable amount of information to work with. This
   means you should provide:

   - Guidance on **how to reproduce the issue**. Ideally, this should be a
     *small* code sample that can be run immediately by the maintainers.
     Failing that, let us know what you're doing, how often it happens, what
     environment you're using, etc. Be thorough: it prevents us needing to ask
     further questions.
   - Tell us **what you expected to happen**. When we run your example code,
     what are we expecting to happen? What does "success" look like for your
     code?
   - Tell us **what actually happens**. It's not helpful for you to say "it
     doesn't work" or "it fails". Tell us *how* it fails: do you get an
     exception? A hang? A non-200 status code? How was the actual result
     different from your expected result?
   - Tell us **what version of Requests you're using**, and
     **how you installed it**. Different versions of Requests behave
     differently and have different bugs, and some distributors of Requests
     ship patches on top of the code we supply.

   If you do not provide all of these things, it will take us much longer to
   fix your problem. If we ask you to clarify these and you never respond, we
   will close your issue without fixing it.
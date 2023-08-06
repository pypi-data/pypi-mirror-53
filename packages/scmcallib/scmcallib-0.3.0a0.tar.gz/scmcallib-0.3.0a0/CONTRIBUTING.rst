Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
###########

Please use the `issue tracker`_ for reporting any bugs about the `scmcallib` package. If you are reporting a bug, please include:

* Your operating system name and version.
* The version of MAGICC/SCM that is being used
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.


Fix Bugs
########

Look through the GitLab issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
##################

Look through the GitLab issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
###################

SCM Calibration could always use more documentation, whether as part of the
official SCM Calibration docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
###############

The best way to send feedback is to file an issue at the `issue tracker`_.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.

Get Started!
------------

Ready to contribute? Here's how to set up `scmcallib` for local development.

1. Clone the repository fork locally:

.. code-block:: console

    $ git clone git@gitlab.com/magicc/scmcallib.git
    $ cd scmcallib/


1. Setup the environment needed to run the code. We use a Makefile to setup the development environment and
installing dependencies. This will try and use conda if possible to install a number of the dependencies which can result
in some speed improvements. To this end a new conda environment can be created using the following:

.. code-block:: console

    $ conda env create --name scmcallib -f environment.yml
    $ conda activate scmcallib
    $ make update_deps

.. note::

    The first time you may need to run make -B update_deps to force reinstall.

The conda environment needs to be activated before using any of the `make` commands in new shells. This can be done by
running `conda activate scmcallib`.

#. Set the location of your MAGICC executable using the `MAGICC_EXECUTABLE_7` environment variable.
This can be set using the `.env` file.
An example file is given as `.env.sample`.
This file can be copied as `.env` and updated as needed.

#. Create a branch for local development:

.. code-block:: console

    $ git checkout -b name-of-your-bugfix-or-feature


Now you can make your changes locally.

#. When you're done making changes, check that your changes pass the tests and style checks:

.. code-block:: console

    $ make test
    $ make flake8

#. Commit your changes and push your branch to GitLab:

.. code-block:: console

    $ git add .
    $ git commit -m "Your one line description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

#. Submit a pull request through the GitLab website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

#. The pull request should include tests.
#. If the pull request adds functionality, the docs should be updated. Put your new functionality into a function with a docstring, add the feature to the list in README.md, and add the change to CHANGELOG.md under unreleased changes.
#. The pull request should work for 3.5 and 3.6. Check the `pipeline`_ feature on gitlab to see test progress and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests:

.. code-block:: console

    $ python -m unittest tests.test_scmcallib

If significant changes are made to the dependencies, the docker image used to bootstrap the CI build should be updated.
The image is updated using the `build-image` CI job which is run manually from the GitLab pipelines page.
Changes to the Dockerfile will not cause the image to automatically be built.
Note that all branches use the same image.

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in CHANGELOG.rst).
Then run:

.. code-block:: console

    $ git tag vX.Y.Z
    $ git push
    $ git push --tags

The GitLab pipeline will then deploy to PyPI if tests pass.
This is currently not implemented.


.. _issue tracker: https://gitlab.com/magicc/scmcallib/issues
.. _pipeline: https://gitlab.com/magicc/scmcallib/pipelines

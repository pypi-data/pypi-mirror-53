.. highlight:: shell

============
Installation
============


Stable release
--------------

.. warning::

    There are currently no publically released versions of scmcallib so please install from source

To install SCM Calibration, run this command in your terminal:

.. code-block:: console

    $ pip install scmcallib

This is the preferred method to install SCM Calibration, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for SCM Calibration can be downloaded from the `GitLab repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://gitlab.com/magicc/scmcallib
    cd scmcallib

Once you have a copy of the source, you can install `scmcallib` and all the required dependencies. Since `scmcallib`
uses a number of compiled libraries under the hood, it is recommended to use a `conda environment`_ to simplify the
install process and increase the execution speed.

.. code-block:: console

    $ conda env create --name scmcallib -f environment.yml
    $ conda activate scmcallib
    $ make update_deps


.. note::

    `environment.yml` is picked up automatically if you're in the scmcallib directory so be explicit in the call to `conda env create`. The first time you may need to run `make -B update_deps` to force reinstall.


.. warning::

    If using conda, you have to use a conda environment other than `base`.
    This avoids impacting every other installed conda environment.

.. _Conda environment: https://conda.io/docs/user-guide/tasks/manage-environments.html
.. _GitLab repo: https://gitlab.com/magicc/scmcallib
.. _tarball: https://gitlab.com/magicc/scmcallib/tarball/master

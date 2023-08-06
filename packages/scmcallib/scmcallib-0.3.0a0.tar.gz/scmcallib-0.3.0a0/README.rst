scmcallib
=========

.. sec-begin-index

scmcallib is a tool to make it easy to derive parameter sets for Simple Climate Models (SCMs).
At the moment, the two focus use cases are:

    - "emulation" of other, typically more complex and computationally expensive models
    - "calibration" to observations i.e. the derivation of parameter sets which allow the SCM response to span the range of uncertainty of historical observations

This package fits into a wider ecosystem of tools which are aiming to create a transparent and reproducible way of generating parameter sets for a wide range of SCMs, observations and climate model outputs in a number of use cases.
scmcallib uses `openscm`_ and `netcdf-scm`_ to make it easy to interface to a range of SCMs and climate model output, hiding the complexity of running these 'simple' climate models and processing complex model output.

.. _openscm: https://github.com/openclimatedata/openscm
.. _netcdf-scm: https://github.com/znicholls/netcdf-scm
.. sec-end-index

Getting Started
---------------

.. sec-begin-getting-started

A number of the libraries used in `scmcallib` require compiled libraries and other system dependencies.
To make it easier to get started with this project it is recommended to set up a new Conda environment to isolate these libraries.
As this package is not currently installable via pypi, you have to install it from source.

.. code-block:: console

    $ git clone git://gitlab.com/magicc/scmcallib
    $ cd scmcallib
    $ conda env create --name scmcallib --file environment.yml
    $ conda activate scmcallib
    $ pip install -e .

Having installed, the scmcallib package is ready to generate parameter sets.

Emulation
#########

Emulation is the process of finding a set of parameters which best fit output from another model.
Once this best fit point in parameter space has been found, the SCM provides a computationally cheap method for exploring how the these larger models would respond under various scenarios.

TODO: Add documention about extracting

Before we can start emulating a model we must define the initial guess of the parameter distributions (i.e. the priors), for the parameters that are being constrained.

[TODO: decide whether to put this example in e.g. a notebook so it's under CI]

.. code-block:: python

    from scmcallib import ParameterSet

    best_guess_c1 = 0.631
    best_guess_c2 = 0.429
    best_guess_a1 = 0.2240

    param_set = ParameterSet()
    param_set.set_tune('c1', Bound(Normal(mu=best_guess_c1, sd=1.), lower=0.1))
    param_set.set_tune('c2', Bound(Normal(mu=best_guess_c2, sd=0.1), lower=0.1))
    param_set.set_tune('a1', Bound(Normal(mu=best_guess_a1, sd=0.1), lower=0.0, upper=0.4))

Once we have the data and parameters which describe how the model will be constrained, we can instantiate the PointEstimateFinder.
In this example we are using the A5IR SCM [TODO: fill out AR5IR SCM so it actually is the full things], a basic, but very fast model to speed up to emulation process.
The first step in emulation is finding the initial starting point for optimisation.
This start point is then used by the optimiser to find the point in parameter space which minimise the differences between the SCM output and the target timeseries (typically taken from a more complex model).

.. code-block:: python

    from scmcallib import PointEstimateFinder
    from scmcallib.scm import AR5IR_SCM
    emulator = PointEstimateFinder(param_set, reference_period=(2000, 2010))
    emulator.set_target(observed=observed_gmt)

    with AR5IR_SCM() as scm:
        results = emulator.find_best_fit(scm, optimiser_name='bayesopt')

    results.plot_summary()
    results.plot_fit()

``scmcallib`` provides a method for reading ``tuningcore`` files which are used by ``simcap`` to describe
how to tune magicc.

Calibration
###########

Run simple calibration example

* edit `calibration.py` and `run_calibration.py` to fit your personal settings
* then run `python run_calibration.py`
* visualise with `notebooks/show_calibration.ipynb`

.. sec-end-getting-started

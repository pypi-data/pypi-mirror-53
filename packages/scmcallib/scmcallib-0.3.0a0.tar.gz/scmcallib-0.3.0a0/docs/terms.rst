.. _terms:

Terms
-----

A number of key scmcallib terms are widely used in a number of contexts, and have a different meaning in each of them.
Here we define the meaning of these terms in the scmcallib context.

model
    A climate model is a 'thing' (for want of a better word) which takes in a number of inputs (emissions timeseries, parameter values) and returns a number of outputs (climate variables like surface temperature, radiative forcing, atmospheric concentrations).

emulation
    Reproducing the behaviour of one model with another.
    In the scmcallib context, when we emulate a more complex model with a simpler one, this means that we find the point in the simple climate model's parameter space which allows it to best reproduce the behaviour of the more complex model (the user can specify the metric which is used to define 'best reproduce').
    In the scmcallib context, emulation always refers to finding single points in parameter space.

calibration
    Determining the region of parameter space which allows a model to best reproduce the span seen in some target distribution.
    In the scmcallib context, this almost always means determining the distribution of parameters in a simple climate model's parameter space which allows it to best reproduce the range and uncertainty of historical observations of climate metrics.

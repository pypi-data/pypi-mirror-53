scikit-learn sidekick
=======================

A wrapper for scikit-learn that makes it easier to write, tune and evaluate classification and regression systems


Installation
-----------------

Install from the python package index:

``pip install sklearnsk``

Or clone this repository and install:

``pip install .``


Usage
-----

TODO


Defining your classification or regression algorithm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The **ConfigurableAlgorithm** abstract class provides a template for implementing your classification or regression algorithm.
If you follow this template, then you will be able to easily tune and evaluate your algorithm without writing a lot of additional,
repetitive code.

The main idea of this template is that it forces you to create a class that has a consistent interface: all algorithms
must have a fit and a predict method, and must be able to be instantiated with a single property; a config dictionary.

This config dictionary is where you define:

* the underlying classification or regression algorithm you use (e.g. SVC, RandomForest, LinearRegression, etc)
* any hyper-parameters involved in tuning the algorithm (e.g. C, gamma, max_depth)
* the individual features or feature groups you might want to turn on or off
* any parameters involved in generating features (e.g. ngram range, max K for K-best feature selection, etc)

Basically, if there are any knobs at all that you would want to fiddle with for tuning your system or performing any feature
analysis, you should be able to manipulate them by changing the config dictionary.

When you implement ConfigurableAlgorithm, you must implement the following methods:


get_default_config()

Should return a dictionary associating keys with default values. The config dictionary used to instantiate the Algorithm
will be merged with this dictionary, so that the.

In particular, this dictionary should provide


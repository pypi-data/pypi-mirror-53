.. _scikit-learn: http://scikit-learn.org/stable/

.. _introduction:

============
Introduction
============

Model search result and reporting
---------------------------------

The class ``GridSearchCV`` of scikit-learn_ provides
an easy way to get the cross-validation scores of an 
estimator for a grid of hyper-parameters. While this is 
a usefull feature, an often scenario in machine learning 
research is to design experiments where multiple estimators
are compared for various hyper-parameter grids. This functionality 
is supported from research-learn by providing the 
:class:`ModelSearchCV` class and the :func:`report_model_search_results` 
function.

Design and analysis of experiments
----------------------------------

Setting up and analyzing the results of machine learning experiments 
is a time consuming procedure that requires multiple steps like
data gathering and preparation, selection of estimators and their
hyperparameters, analysis of the results and finally application of 
multiple statistical tests. The application of these steps is simplified 
by research-learn through the base :class:`BaseExperiment` as well as 
appropriate functions to analyze the experimental results.



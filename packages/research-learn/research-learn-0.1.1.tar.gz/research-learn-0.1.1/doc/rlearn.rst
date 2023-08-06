.. _scikit-learn: http://scikit-learn.org/stable/

.. _rlearn:

==============
research-learn
==============

.. currentmodule:: rlearn

A practical guide
-----------------

The :class:`ModelSearchCV` provides an easy way to search for the model
with the highest cross-validation score. A grid of models and hyper-parameters
is defined and then the ``fit`` method is invoked::

   >>> from sklearn.datasets import load_iris
   >>> from sklearn.neighbors import KNeighborsClassifier
   >>> from sklearn.tree import DecisionTreeClassifier
   >>> from rlearn.model_selection import ModelSearchCV
   >>> X, y, *_ = load_iris().values()
   >>> estimators = [('kn', KNeighborsClassifier()), ('dt', DecisionTreeClassifier())]
   >>> params_grids = [{'kn__n_neighbors': [2, 6]}, {'dt__max_depth': [3, 4]}]
   >>> model_search_cv = ModelSearchCV(estimators, params_grids, scoring='accuracy', cv=5, n_jobs=-1)
   >>> model_search_cv.fit(X, y)
   ModelSearchCV(...)


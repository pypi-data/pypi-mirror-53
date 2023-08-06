======
@model
======


.. image:: https://img.shields.io/pypi/v/atmodel.svg
        :target: https://pypi.python.org/pypi/atmodel

.. image:: https://img.shields.io/travis/eghuro/atmodel.svg
        :target: https://travis-ci.org/eghuro/atmodel

.. image:: https://readthedocs.org/projects/atmodel/badge/?version=latest
        :target: https://atmodel.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Create models with less code.


* Free software: MIT license
* Documentation: https://atmodel.readthedocs.io.


Getting started
---------------
Install @model from pip:

   pip install atmodel


Using @model is as simple as::

  from atmodel import model

  @model('a', optional=['b'])
  class Model:
      pass

Then use the class as::

   m = Model(a=1)
   if m.a() > 0:
       n = Model(a=1, b=2)


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

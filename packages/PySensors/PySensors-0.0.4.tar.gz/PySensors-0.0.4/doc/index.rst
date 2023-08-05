
Welcome to PySensors's documentation!
=====================================

Contents:

.. toctree::
   :maxdepth: 2


Overview
========


Requirements
------------

* Python >=3.6,
* version >=3.x of :file:`libsensors.so` from ``lm-sensors``.


Executing the package as program
================================

.. module:: sensors.cli

The :mod:`sensors.cli` module can be started as a program with the :option:`!-m`
command line option of Python.  It simply…


The :mod:`sensors` package
==========================

.. module:: sensors


:class:`Chip` objects
---------------------

.. class:: Chip


:class:`Feature` objects
------------------------

.. class:: Feature


:class:`Subfeature` objects
---------------------------

.. class:: Subfeature


Environment
===========

The :envvar:`SENSORS_LIB` environment variable can be used to set the path to
the shared library used by PySensors.


License
=======

LGPL v2.1 or later.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


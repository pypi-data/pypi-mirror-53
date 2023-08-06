=============
Data Analysis
=============

Start by importing analysis submodule for Icarus Pressure Jump for NMR .

.. code-block:: python

  from icarus_nmr import analysis

Next step is to create an instance of the Dataset class.

.. code-block:: python

  dataset = analysis.Dataset()
  dataset.folder = 'path/to/the/folder/containing/log/data'
  dataset.description = 'you can write your description here.'
  dataset.init()

The Dataset Class
-------------------------

.. autoclass:: icarus_nmr.analysis.Dataset
  :members:

.. IntertwiningWavelet documentation master file, created by
   sphinx-quickstart on Wed Feb 14 15:27:04 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to IntertwiningWavelet's documentation!
===============================================

This toolbox is dedicated to a method called IntertwiningWavelet (IW) which provides a multiresolution analysis on non oriented graphs. It provides a wavelet basis on a graph and can analyse a banch of signals defined on this graph. 

The method is fully described and analysed in [cit2]_, [cit3]_ and a quicker description can be found in [cit1]_. The approach relies on probabilistic tools: a random spanning forest to downsample the set of vertices, and approximate solutions of Markov intertwining relation [cit3]_ to provide a subgraph structure and a filterbank which is a basis of the set of functions. As a by-product, the method provides a graph coarse-graining procedure.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Home <self>
   tutorials/index
   reference/index
   



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

References
==========

.. toctree::  
   :maxdepth: 2

   references



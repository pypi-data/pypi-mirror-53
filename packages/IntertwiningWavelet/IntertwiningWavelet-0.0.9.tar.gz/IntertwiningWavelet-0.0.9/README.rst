This package, as well as the **IntertwiningWavelet**,  ``iw`` toolbox, is Free software, released under BSD License.

Documentation is available  on the public site at `intertwiningwavelet doc <http://archimede.pages.math.cnrs.fr/intertwiningwavelet>`_.

The latest version of **IntertwiningWavelet**,  is available on the `gitlab repository <https://plmlab.math.cnrs.fr/archimede/intertwiningwavelet>`_ , which provides the git repository managing the source code and where issues can be reported.

The **IntertwiningWavelet** package is a  Python Package for wavelet analysis on graphs.
This toolbox is dedicated to a method called IntertwiningWavelet (IW) which provides a multiresolution analysis on non oriented graphs. It provides a wavelet basis on a graph and can analyse a banch of signals defined on this graph. 

The method is fully described and analysed in `Intertwining wavelets or Multiresolution analysis on graphs through random forests. <https://www.sciencedirect.com/science/article/abs/pii/S1063520318300940>`_, `Approximate and exact solutions of intertwining equations through random spanning forests. <https://arxiv.org/abs/1702.05992>`_ and a quicker description can be found in `Random forests and Network analysis. <https://link.springer.com/article/10.1007/s10955-018-2124-8>`_. The approach relies on probabilistic tools: a random spanning forest to downsample the set of vertices, and approximate solutions of Markov intertwining relation  to provide a subgraph structure and a filterbank which is a basis of the set of functions. As a by-product, the method provides a graph coarse-graining procedure.

The original ``iw`` Toolbox is developed in Python/Cython at `LabEx Archimède <http://labex-archimede.univ-amu.fr/>`_ , as a `I2M <http://www.i2m.univ-amu.fr//>`_ project.

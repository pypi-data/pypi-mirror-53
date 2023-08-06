
=======================================
Install IntertwiningWavelet
=======================================

IntertwiningWavelet toolbox is a Python API developed for Python
3.x 

A large part of the module is developed in Cython, and although the
".c" are provided as sources it can be useful to cythonnize cython code, so
the installation of Cython has to be performed.

To sum up what you need to run the toolbox

- Python 3 is required. Download and install `Python 3 <https://www.python.org/downloads/>`_.
- Cython has to be installed. See `Cython Installation <https://cython.readthedocs.io/en/latest/src/quickstart/install.html>`_.
- GCC is also mandatory to compile C kernel.


Launching the setup tool
------------------------
Run in a terminal the following command

.. code-block:: shell 

	$ python3 setup.py build_ext --inplace

Path to the iw toolbox
----------------------
Open your favorite IDE or Python console and add the path of the toolbox in your python path.




====================================
First steps with IntertwiningWavelet 
====================================

Graph representation
--------------------


The toolbox implements a method called IntertwiningWavelet (IW) which provides a multiresolution analysis on non oriented graphs. It provides a wavelet basis on a graph and can analyse a banch of signals defined on this graph.

The basic object is a graph :math:`(V,w)` where 

-:math:`V` is the set of vertices indexed here from :math:`1` to :math:`n`.

-:math:`w:V\times V\rightarrow \mathbb{R}^+` is the weight function, :math:`w(x,y)` encoding the strength of connexion from vertex :math:`x` to vertex :math:`y`. Two different vertices :math:`x` and :math:`y` are called neighbours if :math:`w(x,y)>0`.

*Watch out that the graph needs to be reversible which means that one can find a measure* :math:`\mu` *on* :math:`V` *such that for each* :math:`x` *and* :math:`y` *in* :math:`V` *we have* :math:`\mu(x)w(x,y)=\mu(y)w(y,x)`. *In case of a non oriented graph this condition is automatically satisfied and the measure* :math:`\mu` *is the uniform measure on* :math:`V`.

The graph is encoded by its Laplacian matrix :math:`L` whose non diagonal entries are :math:`w(x,y)\geq 0` and diagonal entries are :math:`w(x)  =  -\sum\limits_{x\neq y}w(x,y)`.


Our toolbox uses a special graph file format we call a .g file (actually the .g extension in the name of the file is not mandatory). For each vertex, it lists the number of its neighbours, the indices of the neighbours and the corresponding weight function value.

An example of such a file is available here :download:`Torus16 <../../iw/data/tore1d16.g>`.

From a sparse matrix whose outdiagonal values are :math:`w(x,y)` for :math:`x\neq y`, the following code :download:`write_dot_g_sparse.py <./write_dot_g_sparse.py>` writes the .g file (courtesy B. Stordeur). 



Introduction to this tutorial
-----------------------------

*The Python File* :download:`User_Example1.py <./User_Example1.py>` *can be downloaded. It runs the code of this tutorial.*

This tutorial will show you how to use the toolbox on the reference graph :download:`Torus16 <../../iw/data/tore1d16.g>`

This graph connects each of its 16 vertices with two neighbours. Its Laplacian matrix is

.. math::

 	L =  \begin{bmatrix}
              -2 & 1  & 0 & 0 & 0 & ... & 1\\\\
	       1 & -2 &1  & 0 &  0 &... & 0\\\\
               0 & 1  &-2 & 1 &  0 &... & 0\\\\
	       0 &0   &1  &-2& 1& ...& 0\\\\
	       ... &... &...  &...& ...& ...& 0\\\\
               1& 0 &...  &...& ...& 1& -2 
           \end{bmatrix}


We start with a quick description of the outputs of the main class ``IntertwiningWavelet`` and show how to process a signal.

Getting started
---------------

**Load Python modules**

The following Python modules should be useful. 

- scipy.sparse since we will use sparse matrices, 
- NumPy since we will process matrices and arrays, 
- matplotlib.pyplot for visualization

.. code-block:: python

   >>> import numpy as np
   >>> import scipy.sparse as sp
   >>> import matplotlib.pyplot as plt

**Load the graph file**

.. code-block:: python
  
   >>> from iw.data.get_dataset_path import get_dataset_path
   >>> graph_file = get_dataset_path("tore1d16.g")


**Start the instances of IntertwiningWavelet**

.. code-block:: python

   >>> from iw.intertwining_wavelet import IntertwiningWavelet
   >>> iw = IntertwiningWavelet(graph_file)
   "The graph is reversible the pyramide algorithm....
                   can proceed" 
   >>> print(iw.pretreatment) # To check if the graph has the required reversibility (symmetry)
   True
 



**Process the method**

Here we choose to have two levels of decomposition, i.e two levels of details. We could also decide the approximate cardinality of the set of approximation coefficients.

.. code-block:: python

   >>> iw.process_analysis(mod='step', steps=2) # To have two levels of decomposition, i.e 2 levels of details
   >>> print(iw.process_analysis_flag) # True if the decomposition process has been done.
   True
 
   
.. _User_exemple1:

Graphs and subgraphs
--------------------

We start with the main attribute ``tab_Multires`` of ``iw`` which contains the sequence of subgraphs and which also contains the basis.

.. code-block:: python

   >>> tab=iw.tab_Multires

The variable ``tab`` is a MemoryView which has three attributes.

.. code-block:: python

   >>> print(tab)
   <iw.multiresolution.struct_multires_Lbarre.Tab_Struct_multires_Lbarre object at 0x7f3186287e30>


**The attribute** ``steps``: it is the number of decomposition levels.

.. code-block:: python

   >>> print(tab.steps) # To get the number of decomposition levels
   2


**The attribute** ``Struct_Mres_gr``:  it is the sequence of subgraphs which is as well a MemoryView. You can access to the different levels as follows:

.. code-block:: python

   >>> subgraphs = tab.Struct_Mres_gr # To get the sequence of subgraphs
   >>> j0 = 0
   >>> Sg = subgraphs[j0] # To get access to the subgraph at level j0+1


At each level ``j0`` it is possible to get:

- **the list of vertices of the subgraph.** It is again a MemoryView to save memory. You can access the information using NumPy

.. code-block:: python

   	>>> print(np.asarray(Sg.Xbarre)) # Indices of the vertices of the subgraph, drawn from the vertices of the seminal graph
   	[ 0  1  3  4  5  7 10 14 15]
	>>> # Recall that the subsampling of vertices is one realization of a random point process. The result changes each time you launch iw.process_analysis

*Watch out that if the level is not* ``j0  =  0`` *but* ``j0>0`` *the indices in* ``Sg.Xbarre`` *are taken among the set {0,.. nbarre-1} with nbarre the number of vertices of the graph at level j0-1. In other words the set* ``Sg.Xbarre`` *is not given as a subset of the vertices of the original graph, but of the graph it was drawn from.*

.. code-block:: python

	>>> ind_detailj0=np.asarray(Sg.Xbarre) 
	>>> # Indices of the vertices of the subgraph, drawn from the vertices of the seminal graph
	>>> if j0>0: # To recover the indices in the original graph
    		for i in range(j0-1,-1,-1): 
        	Xbarrei=np.asarray(subgraphs[i].Xbarre)
        	ind_detailj0=Xbarrei[ind_detailj0].copy()
	



- **the Laplacian matrix encoding the weights of the subgraph.** It is the generator of a continuous Markov chain, so this is a matrix based on the vertices of the subgraph and whose non diagonal entries are :math:`w(x,y)\geq 0` and diagonal entries are :math:`w(x)  =  -\sum\limits_{x\neq y}w(x,y)`

You can access to it as a sparse matrix. The fields ``Sg.rowLbarres, Sg.colLbarres, Sg.shapeLbarres`` allow it.

.. code-block:: python

   	>>> Lbarre0s = Sg.Lbarres
   	>>> print(Lbarre0s) # It is again a MemoryView
        <MemoryView of 'ndarray' object>
	>>> # Let us get the sparse matrix
        >>> Lbarre0ms =  sp.coo_matrix((Lbarre0s,( Sg.rowLbarres, Sg.colLbarres)),
            shape=(Sg.shapeLbarres, Sg.shapeLbarres))  
	>>> plt.figure() # Let us visualize the non vanishing coefficients
	>>> plt.spy(Lbarre0ms, markersize=2) 
	>>> plt.title('Localization of non vanishing entries')
	>>> plt.xlabel('Indices')
	>>> plt.show()


.. figure:: ./images/spy_sub_graph_16.png
	:scale: 50 %

	Localization of the non vanishing coefficients of the Laplacian of the subgraph.

*Watch out that the Laplacian matrix of the graph is computed through a sparsification step from another Laplacian matrix, the Schur complement of the original Laplacian. The latter is also stored in* ``Sg`` *under the field* ``Sg.Lbarre``

.. code-block:: python

   	>>> Lbarre0 = Sg.Lbarre
   	>>> print(Lbarre0) # It is again a Memory view
        <MemoryView of 'ndarray' object>
	>>> # Let us get the sparse matrix
        >>> Lbarre0m = sp.coo_matrix((Lbarre0,( Sg.rowLbarre, Sg.colLbarre)),
            shape=(Sg.shapeLbarre, Sg.shapeLbarre))  
	>>> sp.linalg.norm(Lbarre0m-Lbarre0ms) # check the difference between the Schur complement and its sparsified version
	0 
	>>> # Here the Schur complement and its sparsified version are the same.

Analysis and reconstruction operators
-------------------------------------

We come back to the attributes of ``tab``.

The third attribute of ``tab`` is ``Struct_Mana_re``. It is again a MemoryView object.

.. code-block:: python

   	>>> basis = tab.Struct_Mana_re
	>>> print(basis)
	<MemoryView of 'ndarray' object>
	>>> l0 = 0 # To access to the functions of the first level (finest scale)
	>>> a0 = basis[l0] 

The attributes of ``basis`` store all the operators needed to analyse signals, ie. to compute wavelets coefficients, and the operators to reconstruct the signals given coefficients. 

These objects beeing slightly more complicated to handle and not really useful in this experiment we do not explore them now more in details. If you want to know more there is a dedicated tutorial :ref:`User_exemple_analysis_recons`.

Process a signal
----------------

Computation of intertwining wavelet coefficients.
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

We will now process a signal. 

**Signal input:** this is here a simple step function. To be processed by ``iw`` it has to be a 2d Numpy array, with possibly just one line.

.. code-block:: python

	>>> n = 16
	>>> Sig = np.zeros((1,n)) # Sig has to be a 2d NumPy array, here with just one line
	>>> Sig[0,0:n//2] = 1
	>>> print(Sig)
	[[1. 1. 1. 1. 1. 1. 1. 1. 0. 0. 0. 0. 0. 0. 0. 0.]]

Let us have a look on it.

.. code-block:: python

	>>> plt.figure()
	>>> plt.plot(Sig[0,:]) # Watch out that Sig is a 2d NumPy array
	>>> plt.title('Original signal')
	>>> plt.show()


.. figure:: ./images/Sig_16.png
	:scale: 50 %

	Original signal.

**Computation of the intertwining wavelet coefficients:** 

This is done using the attribute of ``iw`` which is ``process_coefficients``. The output is a 2d NumPy array, with possibly one line.

.. code-block:: python

	>>> coeffs_iw = iw.process_coefficients(Sig)
	>>> print(coeffs_iw.shape)
	(1, 16)
	>>> print(coeffs_iw) # coeffs is again a 2d NumPy array
	[[-2.55845734e-03 -1.78582022e-02  1.25000130e-01  1.78582022e-02
   	4.16493056e-04  4.16493056e-04  2.55845734e-03  1.84741585e-02
   	8.56532883e-01  9.78647881e-01  9.99267234e-01  9.99456183e-01
   	9.95570764e-01  8.68070076e-01  1.15588087e-02  2.15887658e-02]]

**Organization of the intertwining wavelet coefficients:** 

The organization of the intertwining wavelet coefficients (IW coefficients) in the NumPy array ``coeffs_iw`` is as follows:

	``coeffs_iw``:math:`=[[g_1,g_2,\dots,g_K,f_K]]` 

with 

- :math:`g_1`: the sequence of coefficients of the finest details level,  
- :math:`g_K`: the sequence of coefficients of the coarsest details level, 
- :math:`f_K` the sequence of scaling coefficients, or so called approximation coefficients.

The attribute ``following_size`` of ``iw`` gives the number of coefficients in each layer

.. code-block:: python

	>>> levels_coeffs = np.asarray(iw.following_size)
	>>> print(levels_coeffs)
        [7 1 8]
	

In our example 

- the finest details level :math:`g_1` has 7 coefficients, 
- the coarsest details level :math:`g_2` has 1 coefficients 
- we have 8 approximation coefficients in :math:`f_2`. 

We can also try to guess it on the plot of the IW coefficients since the details coefficients almost vanish.

	>>> plt.figure()
	>>> plt.plot(coeffs_iw[0,:],'*') # Watch out that coeffs is a 2d NumPy array
	>>> plt.title('Intertwining wavelet coefficients')
	>>> plt.show()


.. figure:: ./images/Coeffs_16.png
	:scale: 50 %

	IW coefficients.

*Remember our method is based on a random subsampling and thus the number of coefficients in each layer generally changes at each new run of* ``iw``. *But we compute a basis and thus the total number of coefficients is always the total number of vertices in the graph.*

Reconstruction of signals.
<<<<<<<<<<<<<<<<<<<<<<<<<<

The reconstruction of a signal from its IW coefficients is done using the attribute ``process_signal`` of ``iw``.

**Reconstruction from the scaling coefficients.**

Let us look at the signal whose coefficients are the scaling coefficients. We will keep the 8 last coefficients, and put 0 for the other ones.

.. code-block:: python

	>>> coeffs_approx = np.zeros((1,n))
	>>> napprox = levels_coeffs[tab.steps]
	>>> coeffs_approx[0,n-napprox:n] = coeffs_iw[0,n-napprox:n].copy() # these are the f_2 coefficients
	>>> plt.figure()
	>>> plt.plot(coeffs_approx[0,:],'*')
	>>> plt.show()

.. figure:: ./images/Coeffs_approx_16.png
	:scale: 50 %

	Approximation coefficients.

Let us compute the approximation part from its scaling coefficients.

.. code-block:: python

	>>> approx = iw.process_signal(coeffs_approx)
	>>> plt.figure()
	>>> plt.plot(approx[0,:])
	>>> plt.title('approximation part')
	>>> plt.show()


.. figure:: ./images/Sig_approx_16.png
	:scale: 50 %

	Approximation part: the vertex 15 and 0 are connected so we have a boundary effect on the approximation.

**Reconstruction from the finest detail coefficients.**

We need to extract the 7 first IW coefficients which corresponds to the finest detail coefficients.

.. code-block:: python

	>>> coeffs_detail1 = np.zeros((1,n))
	>>> ndetail1 = levels_coeffs[0]
	>>> coeffs_detail1[0,0:ndetail1] = coeffs_iw[0,0:ndetail1].copy() # these are the g_1 coefficients
	>>> print(coeffs_detail1)
	[[-0.00255846 -0.0178582   0.12500013  0.0178582   0.00041649  0.00041649
   	0.00255846  0.          0.          0.          0.          0.
   	0.          0.          0.          0.        ]]	

Let us compute the finest detail contribution from its coefficients.

.. code-block:: python

	>>> detail1 = iw.process_signal(coeffs_detail1)
	>>> plt.figure()
	>>> plt.plot(detail1[0,:])
	>>> plt.plot(Sig[0,:],'--r')
	>>> plt.title('finest detail part')
	>>> plt.show()


.. figure:: ./images/Sig_detail1_16.png
	:scale: 50 %

	Finest detail part in blue, in red is the original signal. The detail part is localized and does not vanish on the discontinuity.


**Reconstruction from the coarsest detail coefficients.**

We need to extract the coefficients corresponding to the coarsest detail level.

.. code-block:: python

	>>> coeffs_detail2 = np.zeros((1,n))
	>>> coeffs_detail2[0,ndetail1:n-napprox] = coeffs_iw[0,ndetail1:n-napprox].copy() # these are the g_2 coefficients
	>>> print(coeffs_detail2)
	[[0.         0.         0.         0.         0.         0.
  	0.         0.01847416 0.         0.         0.         0.
  	0.         0.         0.         0.        ]]

Let us compute the coarsest detail contribution from its coefficients

.. code-block:: python

	>>> detail2 = iw.process_signal(coeffs_detail2)
	>>> plt.figure()
	>>> plt.plot(detail2[0,:])
	>>> plt.title('coarsest detail part')
	>>> plt.show()


.. figure:: ./images/Sig_detail2_16.png
	:scale: 50 %

	Coarsest detail part. We have some boundary effects due to the connection between vertex 15 and vertex 0 in the original graph.

**Exact reconstruction of the signal.**

As we expect the sum of the approximation, finest and coarsest detail parts, yields the signal, since we do not take into account insignificant numerical errors.

.. code-block:: python

	>>> Sig_L = detail1 + detail2 + approx
	>>> plt.figure()
	>>> plt.subplot(2,1,1)
	>>> plt.plot(Sig_L[0,:])
	>>> plt.subplot(2,1,2)
	>>> plt.plot(np.abs(Sig_L[0,:]-Sig[0,:]))
	>>> plt.show()

.. figure:: ./images/Sig_L.png

	On top the sum of the approximation, finest and coarsest details parts. Below the error between this reconstructed signal and the original one.


*The attribute* ``process_reconstruction_signal`` *of* ``iw`` *uses the analysis and reconstruction operators to compute the wavelet coefficients of the signal and reconstruct it from them. This is equivalent to run* ``iw.process_coefficients`` *and then* ``iw.process_signal`` *starting from the original signal.*

.. code-block:: python

	>>> coeffs_iw = iw.process_coefficients(Sig)
	>>> Sig_R = iw.process_signal(coeffs_iw)
	>>> Sig_r = iw.process_reconstruction_signal(Sig)
	>>> plt.figure()
	>>> plt.subplot(2,1,1)
	>>> plt.plot(Sig_R[0,:]-Sig_r[0,:])
	>>> plt.subplot(2,1,2)
	>>> plt.plot(np.abs(Sig_R[0,:]-Sig[0,:]))
	>>> plt.show()    

.. figure:: ./images/Sig_R.png

	On top the difference between the signal reconstructed from ``coeffs`` and the output of ``iw.process_reconstruction_signal(Sig)``. Below the error between this reconstructed signal and the original one.




.. note::

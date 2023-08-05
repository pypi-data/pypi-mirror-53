# -*- coding: utf-8 -*-
# ######### COPYRIGHT #########
#
# Copyright(c) 2019
# -----------------
#
# * LabEx Archimède: http://labex-archimede.univ-amu.fr/
# * Institut de Mathématique de Marseille : http://www.i2m.univ-amu.fr//
#
# Contributors:
# ------------
#
# * Fabienne Castell <fabienne.castell_AT_univ-amu.fr>
# * Clothilde Mélot <clothilde.melot_AT_univ-amu.fr>
# * Alexandre Gaudilliere <alexandre.gaudilliere_AT_math.cnrs.fr>
# * Dominique Benielli <dominique.benielli_AT_univ-amu.fr>
#
# Description:
# -----------
#
# IntertwiningWavelet is a toolbox in
# python and cython for signal analysis with wavelet on graphs algorithms.
#
# Version:
# -------
#
# * iw version = 0.0.9
#
# Licence:
# -------
#
# License: 3-clause BSD
#
#
# ######### COPYRIGHT #########
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
import scipy.sparse as sp
import cython
import numpy as np
cimport numpy as np


def _sort_oflist(list_to_sparse):
    """ internal function to sort the list

    - Input:

    :param list list_to_sparse: list to sort

    """
    list_to_sparse = sorted(list_to_sparse, key=lambda k: max(k[1], k[2]))
    return list_to_sparse


cpdef tuple sparsify_matrix(double[:] M, long[:] row, long[:] col,
                            int shape, double[:] threshold):
    """ sparsify_matrix function

    - Inputs:

    :param M:  M input matrix 1d sparse matrix to sparsified
    :type M: or array 1d double values
    :param row: row array of sparse matrix M
    :type row: 1d array 1d int_ values
    :param col: column array of sparse matrix M
    :type col: 1d int_ values
    :param shape: shape of M matrix
    :type shape: int
    :param  threshold: array of threshold values
    :type threshold: 1d array 1d double array

    - Output:

    :returns: tuple of (Msparsedata, Msparserow, Msparsecol, shape)
            where  Msparsedata is M sparsified Matrix 
            Msparserow, Msparsecol, shape corresponding row colunms and shape
    :rtype: tuple of array and int value

    """
    # print("dans sparsify_matrix ")
    cdef int i, j
    list_to_sparse = []
    cdef np.ndarray[np.double_t, ndim=1] delta = np.zeros(shape, dtype=np.double)
    cdef np.ndarray[np.int_t, ndim=1]  Msparserow, Msparsecol

    Msp = sp.csr_matrix((M, (row, col)), shape=(shape, shape))
    Msparse = Msp.copy()

    for i, j in zip(row, col):
            if i > j:
                if Msp[i, j] < threshold[i] and Msp[j, i] < threshold[j]:
                    list_to_sparse.append([(i, j), Msp[i, j], Msp[j, i]])
    list_to_sparse = _sort_oflist(list_to_sparse)
    for l in list_to_sparse:
        i = l[0][0]
        j = l[0][1]
        if delta[i] + Msp[i, j] < threshold[i] and delta[j] + Msp[j, i] < threshold[j]:
            delta[i] = delta[i] + Msp[i, j]
            delta[j] = delta[j] + Msp[j, i]
            Msparse[i, j] = 0.0
            Msparse[j, i] = 0.0
        else:
            break

    for i in range(shape):
        Msparse[i, i] = Msparse[i, i] + delta[i]
    sp.csr_matrix.eliminate_zeros(Msparse)
    Msparse = Msparse.tocoo()
    Msparserow = Msparse.row.astype(np.int_)
    Msparsecol = Msparse.col.astype(np.int_)
    return Msparse.data, Msparserow, Msparsecol, shape

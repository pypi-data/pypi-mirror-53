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
import numpy as np
import scipy.sparse as sp
cimport cython
cimport numpy as np


# don’t check for out-of-bounds indexing.
@cython.boundscheck(False)
# assume no negative indexing.
@cython.wraparound(False)
cpdef tuple operateur_reconstruction_one_step(
        double[:] L, long int[:] row_L, long int[:] col_L, int shape_L,
        double[:] Lbarre, long int[:] row_Lbarre,
        long int[:] col_Lbarre, int shape_Lbarre,
        double[:] GXbarrebr, long int[:] row_GXbarrebr,
        long int[:] col_GXbarrebr, int shape_GXbarrebr,
        long int[:] Xbarre,
        double qprime):
    """ operateur_reconstruction_one_step function
    build operator for reconstruction

    - Inputs:

    :param L:  L is the laplacien matrix
    :type L: 1d double array
    :param row_L: row array of sparse matrix L
    :type row_L:  1d int_ array
    :param col_L: column array of sparse matrix L
    :type col_L:  1d int_ array
    :param int shape_L: shape of L matrix
    :param Lbarre:  Lbarre  matrix
    :type Lbarre:  1d double array
    :param row_Lbarre: row array of sparse matrix Lbarre
    :type row_Lbarre: 1d int_ array
    :param col_Lbarre: column array of sparse matrix Lbarre
    :type col_Lbarre: 1d int_ array
    :param int shape_Lbarre: shape of Lbarre matrix
    :param GXbarrebr:  GXbarrebr  matrix
    :type GXbarrebr: 1d double array
    :param row_GXbarrebr: row array of sparse matrix GXbarrebr
    :type row_GXbarrebr: 1d int_ array
    :param col_GXbarrebr: column array of sparse matrix GXbarrebr
    :type col_GXbarrebr: 1d int_ array
    :param int shape_GXbarrebr: shape of GXbarrebr matrix
    :param Xbarre: vector of indices corresponding to approximation indices
    :type Xbarre: 1d int_ array
    :param double qprime: qprime value


    - Output:

    :returns: tuple of (Rbarre, Rbarre_row, Rbarre_col,
            Rbarre_shape0, Rbarre_shape1, Rbreve, Rbreve_row,
            Rbreve_col, Rbreve_shape0, Rbreve_shape1)
            where Rbarre_matrix are rectangular matrix
            for approximation operator and  Rbreve_matrix  for details
            returned in sparse format
    :rtype: tuple 9  arrays

    """
    # print("dans operateur_reconstruction_one_step")
    n = shape_L
    m = Xbarre.size
    sLbarre = sp.csr_matrix(
        (Lbarre, (row_Lbarre, col_Lbarre)), shape=(shape_Lbarre, shape_Lbarre))
    sGXbarrebr = sp.csr_matrix(
        (GXbarrebr, (row_GXbarrebr, col_GXbarrebr)),
        shape=(shape_GXbarrebr, shape_GXbarrebr))
    sL = sp.csr_matrix((L, (row_L, col_L)), shape=(shape_L, shape_L))
    cdef np.ndarray[np.int_t, ndim=1] Xbreve = np.arange(n) 
    cdef np.ndarray[np.int_t, ndim=1] Xr = Xbreve[Xbarre]

    Xbreve = np.delete(Xbreve, Xr)
    mb = Xbreve.size

    m_sGXbarrebr = - sGXbarrebr
    Rbarrei1 = sp.eye(m, m) - (1 / qprime) * sLbarre
    sl_temp = sL[Xbreve, :]
    sl_slice_br = sl_temp[:, Xbarre]

    Rbarrei2 = m_sGXbarrebr.dot(sl_slice_br)

    Rbarrei_s = sp.vstack([Rbarrei1, Rbarrei2])

    sl_temp = sL[Xbarre, :]
    sl_slice_bv = sl_temp[:, Xbreve]
    Rbrevei1 = sl_slice_bv.dot(-sGXbarrebr)
    Rbrevei2 = -1 * sp.eye(mb) + qprime * sGXbarrebr
    Rbrevei_s = sp.vstack([Rbrevei1, Rbrevei2])

    X = np.concatenate((Xbarre, Xbreve))

    Rbarre_s = Rbarrei_s.copy()
    Rbreve_s = Rbrevei_s.copy()
    # Rbarre_s = Rbarrei_s[X, :]
    # Rbreve_s = Rbrevei_s[X, :]
    Rbarre_s[X,:] = Rbarrei_s
    Rbreve_s[X,:] = Rbrevei_s
    Rbarre_s = Rbarre_s.tocoo()
    Rbarre = Rbarre_s.data
    Rbarre_row = Rbarre_s.row.astype(np.int_)
    Rbarre_col = Rbarre_s.col.astype(np.int_)
    Rbarre_shape0 = Rbarre_s.shape[0]
    Rbarre_shape1 = Rbarre_s.shape[1]

    Rbreve_s = Rbreve_s.tocoo()
    Rbreve = Rbreve_s.data
    Rbreve_row = Rbreve_s.row.astype(np.int_)
    Rbreve_col = Rbreve_s.col.astype(np.int_)
    Rbreve_shape0 = Rbreve_s.shape[0]
    Rbreve_shape1 = Rbreve_s.shape[1]
    return (Rbarre, Rbarre_row, Rbarre_col, Rbarre_shape0, Rbarre_shape1,
            Rbreve, Rbreve_row, Rbreve_col, Rbreve_shape0, Rbreve_shape1)

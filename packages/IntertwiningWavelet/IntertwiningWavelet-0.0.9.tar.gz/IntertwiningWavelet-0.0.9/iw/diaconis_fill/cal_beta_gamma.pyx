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
import cython
import numpy as np
import scipy.sparse as sp

cimport numpy as np
ctypedef np.float_t DTYPE_t


# don’t check for out-of-bounds indexing.
@cython.boundscheck(False)
# assume no negative indexing.
@cython.wraparound(False)
cpdef tuple cal_beta_gamma(double[:] L, long[:] row, long[:] col, int shape,
                           double[:] GXbarrebr,
                           long[:] row2, long[:] col2, int shape2,
                           long[:] Xbarre, long[:] Xbreve, double a):
    """cal_beta_gamma function
    Computation of the estimation of gamma and beta


    - Inputs:

    :param L: L is the laplacien matrix L nxn matrix; Markov generator
    :type L: 1d double array
    :param row: row array of sparse matrix L
    :type row: 1d int_ array
    :param col: column array of sparse matrix L
    :type col: 1d int_ array
    :param int shape: shape of Laplacien matrix
    :param GXbarrebr: matrix (-L_Xbreve,Xbreve)^{-1}
    :param row2: row array of sparse matrix GXbarrebr
    :type row2: 1d int_ array
    :param col2: column array of sparse matrix GXbarrebr
    :type col2: 1d int_ array
    :param int shape2: shape of L matrix
    :param Xbarre: vector of nR indices corresponding to the part of matrix L
    :type Xbarre: 1d int_ array
    :param Xbreve: vector of nR-n indices corresponding to complement  of
           Xbarre the root indices
    :type Xbreve: 1d int_ array
    :param double a: maximum rate (maximum of the absolute value of the
                  diagonal coefficients of L)

    - Output:

    :returns: tuple of (gam, beta) where gamma: numeric. 1/gamma= maximum Hitting time
            and beta: the mean of the return time after the first step.
    :rtype: tuple of 2 double values

    """
    Lsp = sp.csr_matrix((L, (row, col)), shape=(shape, shape))
    GXbarrebrsp = sp.csr_matrix((GXbarrebr, (row2, col2)),
                                shape=(shape2, shape2))
    cdef int n
    cdef int r
    # the mean waitting time of R
    cdef double gam
    cdef double beta
    n = shape
    nr = Xbarre.size
    v = np.ones((n-nr))

    Hit = - GXbarrebrsp.dot(v)

    gam = Hit.max()
    gam = 1 / gam
    L_slice = Lsp[Xbarre, :]
    L_slice = L_slice[:, Xbreve]
    betaHit = L_slice.dot(Hit)
    if betaHit.size > 0:
        beta = betaHit.max() / a
        beta = 1 / beta
    else:
        beta = a
    return gam, beta

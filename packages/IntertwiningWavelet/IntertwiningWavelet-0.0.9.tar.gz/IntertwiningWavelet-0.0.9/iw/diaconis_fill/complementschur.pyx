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
import scipy.sparse.linalg as splin

cimport numpy as np
ctypedef np.float_t DTYPE_t
import warnings
warnings.filterwarnings("ignore")


def cal_Laplacian(Lbarre):
    """This function computes the laplacian of the Markov chain given the
    weights matrix, I.e L(x,y)=w(x,y) for x different of y, and L(x,x)=-w(x)
    with w(x)=sum_y w(x,y) as well as alphabarre=max w(x)

    - Input:

    :param Lbarre:  Lbarre is the laplacian matrix

    - Output:

    :returns: tuple of (Lbarre abarre)
            where  Lbarre sparse Laplacian matrix
            abarre value of abarre,
    :rtype: tuple of arrays and double values
    """
    W = Lbarre.copy()
    L = W.copy()
    n, m = Lbarre.shape

    u = np.zeros(n)
    W.setdiag(u, k=0)
    diagonalw = (- W.sum(1)).squeeze()
    diag = np.array(diagonalw.data, dtype=np.float64)
    diag = diag.squeeze()
    L.setdiag(diag, k=0)
    # L = W. sp.spdiags(W, diagonalw, n, m)
    alphabarre = (np.absolute(diagonalw)).max()

    return L, alphabarre

# don’t check for out-of-bounds indexing.
@cython.boundscheck(False)
# assume no negative indexing.
@cython.wraparound(False)
cpdef tuple complementschur(double[:] L, long[:] row, long[:] col, int shape,
                            long[:] R, long[:] Rc):
    """ Schur complement is the computation function
    M of D based on the formula: with

    .. math::

       L =  \\begin{bmatrix}
              A & B \\\\
              C & D
           \\end{bmatrix}



    the Schur complement of D
    is  :math:`SM(D) = A - B D^{-1} C`


    - Input:

    :param L:  L is the laplacien matrix
    :type L: 1d double array
    :param row: row array of sparse matrix L
    :type row: 1d int_ array
    :param col: column array of sparse matrix L
    :type col: 1d int_ array
    :param int shape: shape of L matrix
    :param R: vector of nR indices corresponding to the roots indices
    :type R: 1d int_ array
    :param Rc: vector of nR-n indices corresponding to complement 
             of the root indices
    :type Rc: 1d int_ array

    - Output:

    :returns: tuple of (Lbarre1d, row1, col1, shape1, abarre, GXbarrebr1d, row2, col2, shape2)
            where  Lbarre1d is Schur complement of [L]_Rc in L , row1, col1, shape1,
            corresponding rox, col and shape
            abarre value of abarre,
            GXbarrebr1d  ([L]_Rc)^{-1} 1d sparse matrix , row2, col2, shape2,
            corresponding rox, col and shape
    :rtype: tuple of arrays and double values

    """
    cdef np.ndarray[np.double_t, ndim=1] Lbarre1d

    cdef np.ndarray row1
    cdef np.ndarray col1
    cdef int i
    cdef int tr = R.size
    cdef int trc = Rc.size
    cdef np.ndarray[np.double_t, ndim=1] GXbarrebr1d
    cdef np.ndarray row2
    cdef np.ndarray col2
    cdef int shape1
    cdef int shape2
    cdef double abarre
    cdef double alpha

    Lsp = sp.csr_matrix((L, (row, col)), shape=(shape, shape))
    alpha = np.absolute(Lsp.diagonal()).max()

    A1 = Lsp[R, :]
    A = A1[:, R]
    B = A1[:, Rc]
    C1 = Lsp[Rc, :]
    C = C1[:, R]
    D = C1[:, Rc]
    ##################################################################
    # Matrix Inversion
    ##################################################################
    GXbarrebr = splin.inv(D)
    if len(GXbarrebr.shape) < 2:
        GXbarrebr = sp.csr_matrix(GXbarrebr)
    Lbarre = A - B.dot(GXbarrebr).dot(C)
    ########################################################
    # Fix bug matrix inversion lead to negativ coefficients
    #######################################################
    n, m = Lbarre.shape
    u = np.zeros(n)
    W = Lbarre.copy()
    W.setdiag(u, k=0)
    row_neg, col_neg, neg_values = sp.find(W < 0)
    if neg_values.data.shape[0] > 0:
        max_value = W.max()
        epsilon = np.spacing(max_value)
        if (neg_values > epsilon).size == 0:
            Lbarre[row_neg, col_neg] = 0.0
            sp.csr_matrix.eliminate_zeros(Lbarre)
        else:
            I_D = sp.eye(trc, trc)
            P = 1.0/alpha * D + I_D
            S = I_D.tocsr()
            Pit = I_D.tocsr()
            epsilon = np.spacing(P.max())
            for j in range(trc):
                i = 0
                while np.absolute(Pit[j, :]).sum() > epsilon:
                    i += 1
                    Pit[j, :] = Pit[j, :].dot(P)
                    S[j, :] = S[j, :] + Pit[j, :]
                iterations = i
            sp.csr_matrix.eliminate_zeros(S)
            GXbarrebr = - S / alpha
            Lbarre = A + B.dot(S).dot(C/alpha)

    # for i in range(Lbarre.shape[0]):
    #    Lbarre[i, i] = 0
    # Lbarre = sp.abs(Lbarre)
    # diaglw = sp.sum(Lbarre, 1)
    # for i in range(Lbarre.shape[0]):
    #    Lbarre[i, i] = diaglw[i]

    if min(Lbarre.shape) > 0:
        abarre = np.max(np.abs(Lbarre.diagonal()))
    else:
        abarre = 0
    Lbarre, abarre = cal_Laplacian(Lbarre)
    GXbarrebr = GXbarrebr.tocoo()
    if type(Lbarre) is sp.csr_matrix:
        Lbarre = Lbarre.tocoo()
    else:
        Lbarre = sp.coo(Lbarre)
    Lbarre1d = Lbarre.data
    row1 = Lbarre.row.astype(dtype=np.int_)
    col1 = Lbarre.col.astype(dtype=np.int_)
    GXbarrebr1d = GXbarrebr.data
    row2 = GXbarrebr.row.astype(dtype=np.int_)
    col2 = GXbarrebr.col.astype(dtype=np.int_)
    shape1 = Lbarre.shape[0]
    shape2 = GXbarrebr.shape[0]
    return Lbarre1d, row1, col1, shape1, abarre, GXbarrebr1d, row2, col2, shape2


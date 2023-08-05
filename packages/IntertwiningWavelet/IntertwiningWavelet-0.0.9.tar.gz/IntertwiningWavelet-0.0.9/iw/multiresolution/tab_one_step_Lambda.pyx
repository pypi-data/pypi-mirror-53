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
import math

# don’t check for out-of-bounds indexing.
@cython.boundscheck(False)
# assume no negative indexing.
@cython.wraparound(False)
cpdef  tuple  tab_one_step_Lambda(double a, double[:] L, long[:] row,
                                  long int[:]col, int shape, long[:] Xbarre,
                                  long[:] Xbreve, int n):
    """
    Intermediate function which returns Lambdabarre, Lambdabreve matrix

    - Inputs:

    :param L: L is the laplacien matrix L n x n matrix; Markov generator
    :type L: 1d double array
    :param row: row array of sparse matrix L
    :type row: 1d int_ array
    :param col: column array of sparse matrix L
    :type col: 1d int_ array
    :param int shape: shape of Laplacien matrix
    :param Xbarre: vector of nR indices corresponding to the part of matrix L
    :type Xbarre: 1d int_ array
    :param Xbreve: vector of nR-n indices corresponding to complement  of
           Xbarre the root indices
    :type Xbreve: 1d int_ array
    :param int n: size of the set of vertices

    - Outputs:

    :returns: tuple of (Lambdabarre and its row, col and shapes,
            Lambdabreve ,and its row, col and shapes
            qprime), where matrix whose rows are the nu_xbarre
            and Lambdabreve matrix whose rows are the psi_xbreve
            qprime parameter to compute the solution of
            Diaconis-Fill equation
    :rtype: tuple of arrays and int

    """
    Ls = sp.csc_matrix((L, (row, col)), shape=(shape, shape))
    nbarre = Xbarre.size
    max_value = Ls.max()
    epsilon = np.spacing(max_value)
    qprime = 2 * a * nbarre/(n-nbarre)
    I = sp.eye(n)
    I = I.tocsr()
    D = qprime * I - Ls
    # Green = qprime * sp.linalg.inv(D)
    ###############################################################
    # BugFix zero Laplacian replace inverse by iterartive method 
    ###############################################################
    P_n = 1 / (qprime+a) * Ls + a/(qprime+a) * I

    S = I.copy()

    k0 = math.floor(math.log(epsilon) / math.log(a/(qprime+a))) + 1
    for i in range(k0):
        S = P_n .dot(S) + I
    iterations = i
    Green = qprime * S / (qprime + a)

    Lambdabarre = Green[Xbarre, :]

    Lambdabreve = Green[Xbreve, :] - I[Xbreve, :]

    Lambdabarre = Lambdabarre.tocoo()
    Lambdabreve = Lambdabreve.tocoo()

    return (Lambdabarre.data, Lambdabarre.row.astype(np.int_),
            Lambdabarre.col.astype(np.int_),
            Lambdabarre.shape[0], Lambdabarre.shape[1],
            Lambdabreve.data, Lambdabreve.row.astype(np.int_),
            Lambdabreve.col.astype(np.int_),
            Lambdabreve.shape[0], Lambdabreve.shape[1], qprime)

# don’t check for out-of-bounds indexing.
@cython.boundscheck(False)
# assume no negative indexing.
@cython.wraparound(False)
cpdef tuple tab_compute_sol1_DF_Lambda(double[:] L, long[:] row, long[:] col,
                                       int shape, double a, double qprime,
                                       long[:] R, long[:] Rc):
    """ This function tab_compute_sol1_DF_Lambda is a part of tab_one_step_Lambda
    function

    """
    n = shape
    I = sp.eye(n)
    I = I.tocsr()
    Ls = sp.csr_matrix((L, (row, col)), shape=(shape, shape))
    max_value = Ls.max()
    epsilon = np.spacing(max_value)
    D = qprime * I - Ls
    # Green = qprime * sp.linalg.inv(D)
    ###############################################################
    # BugFix zero Laplacian replace inverse by iterartive method 
    ###############################################################
    P_n = 1 / (qprime+a) * Ls + a/(qprime+a) * I

    S = I.copy()

    k0 = math.floor(math.log(epsilon) / math.log(a/(qprime+a))) + 1
    for i in range(k0):
        S = P_n .dot(S) + I
    iterations = i
    Green = qprime * S / (qprime + a)

    Lambdabarre = Green[R, :]

    Lambdabreve = Green[Rc, :] - I[Rc, :]

    Lambdabarre = Lambdabarre.tocoo()
    listlambda = [Lambdabarre.data, Lambdabarre.row, Lambdabarre.col,
                  Lambdabarre.shape[0], Lambdabarre.shape[1]]
    Lambdabreve = Lambdabreve.tocoo()
    listlambda.append([Lambdabreve.data, Lambdabreve.row, Lambdabreve.col,
                       Lambdabreve.shape[0], Lambdabreve.shape[1]])

    return tuple(listlambda)

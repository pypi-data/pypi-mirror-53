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
cimport iw.multiresolution.struct_multires_Lbarre
from iw.multiresolution.struct_multires_Lbarre cimport Struct_M_ana_recons


# don’t check for out-of-bounds indexing.
@cython.boundscheck(False)
# assume no negative indexing.
@cython.wraparound(False)
cpdef tuple tab_compute_multires_coeffs_sparse(
        double[:] f,
        Struct_M_ana_recons[:] Struct_Mana_re,
        int steps):
    """ Function tab_compute_multires_coeffs_sparse,
    computes the sequence of approximation and detail
    coefficients given the sequence of subgraphs on which the multiresolution
    is to be computed.

    - Inputs:

    :param f:  f is the signal vector
    :type f: 1d double array
    :param Struct_Mana_re: array of :py:class:`iw.multiresolution.struct_multires_Lbarre.Struct_M_ana_recons`
                         class containing reconstruction matrix
                         from :py:data:`iw.multiresolution.struct_multires_Lbarre.Tab_Struct_multires_Lbarre.Struct_Mana_re`
    :type Struct_Mana_re: 1d array of :py:class:`iw.multiresolution.struct_multires_Lbarre.Struct_M_ana_recons`      
    :param int steps: number of multiresolution steps

    - Output:

    :returns: tuple of (coeffs, suite_taille) where coeffs are the coefficients
            array  decomposition of the signal
    :rtype: tuple of one 1d array of double and one 1d array of int

    """
    cdef int i

    cdef np.ndarray[np.double_t, ndim=1] coeffs = np.zeros(0)
    cdef np.ndarray[np.int_t, ndim=1] suite_taille = np.zeros(0, dtype=np.int_)
    fbreve, f = _cal_coeff(f, Struct_Mana_re, 0)
    coeffs = np.concatenate((coeffs, fbreve))
    nd = np.array([fbreve.size], dtype=np.int_)
    suite_taille = np.concatenate((suite_taille, nd))

    if steps == 1:
        coeffs = np.concatenate((coeffs, f))
        n0 = np.array([f.size])
        suite_taille = np.concatenate((suite_taille, n0))
    else:
        for i in range(1, steps):
            fbreve, f = _cal_coeff(f, Struct_Mana_re, i)

            coeffs = np.concatenate((coeffs, fbreve))
            nd = np.array([fbreve.size], dtype=np.int_)
            suite_taille = np.concatenate((suite_taille, nd))

        coeffs = np.concatenate((coeffs, f))
        n0 = np.array([f.size], dtype=np.int_)
        suite_taille = np.concatenate((suite_taille, n0))

    return coeffs, suite_taille


cpdef tuple _cal_coeff(double[:] f, Struct_Mana_re, int step):
    cdef np.ndarray[np.double_t, ndim=1] fbreve
    Lambdabarre = Struct_Mana_re[step].Lambdabarre
    rowla = Struct_Mana_re[step].rowLambdabarre
    colla = Struct_Mana_re[step].colLambdabarre
    shape0la = Struct_Mana_re[step].shape0Lambdabarre
    shape1la = Struct_Mana_re[step].shape1Lambdabarre
    sLambdabarre = sp.csr_matrix(
        (Lambdabarre, (rowla, colla)), shape=(shape0la, shape1la))

    Lambdabreve = Struct_Mana_re[step].Lambdabreve
    rowlb = Struct_Mana_re[step].rowLambdabreve
    collb = Struct_Mana_re[step].colLambdabreve
    shape0lb = Struct_Mana_re[step].shape0Lambdabreve
    shape1lb = Struct_Mana_re[step].shape1Lambdabreve
    sLambdabreve = sp.csr_matrix(
        (Lambdabreve, (rowlb, collb)), shape=(shape0lb, shape1lb))
    fbreve = sLambdabreve.dot(f)
    f = sLambdabarre.dot(f)

    return fbreve, f

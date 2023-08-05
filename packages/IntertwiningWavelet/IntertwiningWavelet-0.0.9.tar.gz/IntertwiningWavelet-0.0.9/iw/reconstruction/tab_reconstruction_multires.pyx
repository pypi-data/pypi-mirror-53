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
cimport cython
import numpy as np
import scipy.sparse as sp
cimport iw.multiresolution.struct_multires_Lbarre
from iw.multiresolution.struct_multires_Lbarre cimport Struct_M_ana_recons


cpdef double[:] tab_reconstruction_multires(double[:] coeffs,
                                        Struct_M_ana_recons[:] Struct_Mana_re,
                                        int steps):
    """
    tab_reconstruction_multires function computes the reconstruction of the signal f from their
    coefficients coeffs

    - Inputs:

    :param coeffs: array of coefficients coefficients
    :type coeffs: 1d array of double
    :param Struct_Mana_re: array of :py:class:`iw.multiresolution.struct_multires_Lbarre.Struct_M_ana_recons` class
                        from :py:data:`iw.multiresolution.struct_multires_Lbarre.Tab_Struct_multires_Lbarre.Struct_Mana_re`
                        , containing different fields of reconstruction matrix decomposition
    :type Struct_Mana_re: 1d array of :py:class:`iw.multiresolution.struct_multires_Lbarre.Struct_M_ana_recons`
    :param int steps: numbers of element present in Struct_Mana_re

    - Output:

    :returns: double array fbarre reconstruction from the different steps of 
            Struct_Mana_re and coeffs
    :rtype: 1d array of double

    """
    cdef int i
    nap = Struct_Mana_re[steps-1].Recons_shape1_barre

    fbarre, coeffs = _cal_fbarre(coeffs, nap)
    fbarre, coeffs = _cal_f(fbarre, coeffs, Struct_Mana_re, steps-1)

    if steps > 1:
        for i in range(steps-2, -1, -1):
            fbarre, coeffs = _cal_f(fbarre, coeffs, Struct_Mana_re, i)

    return fbarre


cpdef tuple _cal_f(double[:] fbarre, double[:] coeffs,
                   Struct_M_ana_recons[:] Struct_Mana_re,
                   int index_step):

    Reconsbarre = Struct_Mana_re[index_step].Reconsbarre
    collra = Struct_Mana_re[index_step].Recons_col_barre
    rowlra = Struct_Mana_re[index_step].Recons_row_barre
    shape0lra = Struct_Mana_re[index_step].Recons_shape0_barre
    shape1lra = Struct_Mana_re[index_step].Recons_shape1_barre

    sRbarre = sp.csr_matrix((Reconsbarre, (rowlra, collra)),
                            shape=(shape0lra, shape1lra))

    Reconsbreve = Struct_Mana_re[index_step].Reconsbreve
    collrb = Struct_Mana_re[index_step].Recons_col_breve
    rowlrb = Struct_Mana_re[index_step].Recons_row_breve
    shape0lrb = Struct_Mana_re[index_step].Recons_shape0_breve
    shape1lrb = Struct_Mana_re[index_step].Recons_shape1_breve

    sRbreve = sp.csr_matrix((Reconsbreve, (rowlrb, collrb)),
                            shape=(shape0lrb, shape1lrb))
    nbr = shape1lrb
    fbreve = coeffs[coeffs.size - nbr: coeffs.size].copy()
    coer = np.arange(coeffs.size - nbr, coeffs.size)
    coeffs = np.delete(coeffs,  coer)

    fbarre = sRbarre.dot(fbarre) + sRbreve.dot(fbreve)
    return fbarre, coeffs

cpdef tuple _cal_fbarre(double[:] coeffs, int nap):
    fbarre = coeffs[coeffs.size - nap: coeffs.size].copy()
    coer = np.arange(coeffs.size - nap, coeffs.size)
    coeffs = np.delete(coeffs, coer)
    return fbarre, coeffs

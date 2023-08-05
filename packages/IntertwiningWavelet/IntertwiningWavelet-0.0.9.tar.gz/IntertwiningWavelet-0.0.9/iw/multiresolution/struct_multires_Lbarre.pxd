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
from iw.graph_c cimport Graph_c
cimport numpy as np

cdef class Struct_multires_Lbarre:

    cdef public double[:] Lbarre
    cdef public long int[:] rowLbarre
    cdef public long int[:] colLbarre
    cdef public int shapeLbarre

    cdef public double[:] Lbarres
    cdef public long int[:] rowLbarres
    cdef public long int[:] colLbarres
    cdef public int shapeLbarres

    cdef public double[:] mubarre
    cdef public long int[:] Xbarre

    cdef public double alphabar
    cdef public double gamma
    cdef public double beta
    cdef public double q
    cdef public double qprime


cdef class Struct_M_ana_recons:
    cdef public double[:]  Lambdabarre
    cdef public long int[:]  rowLambdabarre
    cdef public long int[:]  colLambdabarre
    cdef public int  shape0Lambdabarre
    cdef public int  shape1Lambdabarre

    cdef public double[:]  Lambdabreve
    cdef public long int[:]   rowLambdabreve
    cdef public long int[:] colLambdabreve
    cdef public int  shape0Lambdabreve
    cdef public int shape1Lambdabreve

    cdef public double[:]  Reconsbarre
    cdef public long int[:]   Recons_col_barre
    cdef public long int[:]  Recons_row_barre
    cdef public int    Recons_shape0_barre
    cdef public int   Recons_shape1_barre

    cdef public double[:] Reconsbreve
    cdef public long int[:]   Recons_col_breve
    cdef public long int[:]  Recons_row_breve
    cdef public int   Recons_shape0_breve
    cdef public int   Recons_shape1_breve


cdef class Tab_Struct_multires_Lbarre:
    cdef public Struct_multires_Lbarre[:]  Struct_Mres_gr
    cdef public Struct_M_ana_recons[:]  Struct_Mana_re
    cdef public int steps
    cpdef tuple  _decomposition(self, int i, Graph_c graph, double alphabar0,
                                double[:] mu0, int n0, double theta)


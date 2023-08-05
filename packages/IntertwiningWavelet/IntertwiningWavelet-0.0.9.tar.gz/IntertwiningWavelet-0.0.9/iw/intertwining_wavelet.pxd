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
from iw.multiresolution.struct_multires_Lbarre cimport Tab_Struct_multires_Lbarre
from cpython cimport bool

cdef class IntertwiningWavelet:
    cdef public double[:, :] signals
    cdef public bool pretreatment
    cdef public int nbr_signals
    cdef public Graph_c graph
    cdef public Tab_Struct_multires_Lbarre tab_Multires
    cdef public double[:] mu_initial
    cdef public double[:, :] reconstructed_s
    cdef public double[:, :] coeffs
    cdef public long[:] following_size
    cdef public double a
    cdef public str graph_file_initial
    cdef public bool process_analysis_flag
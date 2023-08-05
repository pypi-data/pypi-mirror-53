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
cimport numpy as np
from iw.multiresolution.struct_multires_Lbarre cimport Struct_M_ana_recons

cpdef double[:] tab_reconstruction_multires(double[:] coeffs,
                                            Struct_M_ana_recons[:] Struct_Mana_re,
                                            int steps)

cpdef tuple _cal_f(double[:] fbarre, double[:] coeffs,
                       Struct_M_ana_recons[:] Struct_Mana_re,
                       int index_step)

cpdef tuple _cal_fbarre(double[:] coeffs, int nap)

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
import unittest


import numpy as np
import scipy.sparse as sp
from iw.diaconis_fill.cal_beta_gamma import cal_beta_gamma


class CalBetaGTest(unittest.TestCase):

    def test_cal_beta_gamma(self):
        L_full = np.array(
         [[-2.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [1.0, -2.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0.0, 1.0, -2.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0.0, 0.0, 1.0, -2.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0.0, 0.0, 0.0, 1.0, -2.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0.0, 0.0, 0.0, 0.0, 1.0, -2.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -2.0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -2, 1.0, 0, 0, 0, 0, 0, 0, 0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -2.0, 1.0, 0, 0, 0, 0, 0, 0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -2.0, 1.0, 0, 0, 0, 0, 0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -2.0, 1.0, 0, 0, 0, 0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -2.0, 1.0, 0, 0, 0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -2.0, 1, 0, 0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -2.0, 1.0, 0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -2.0, 1],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, -2.0]])

        R = np.array([0, 1, 2])

        Xbarre = np.array(R, dtype=np.int_)
        Rc = np.array([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        Xbreve = np.array(Rc, dtype=np.int_)

        a = 1.5

        GXbarrebr_full = np.array(
         [[-0.50000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000],
          [0.00000, -0.50000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000],
          [0.00000, 0.00000, -0.91667, -0.83333, -0.75000, -0.66667, -0.58333, -0.50000, -0.41667, -0.33333, -0.25000, -0.16667, -0.08333],
          [0.00000, 0.00000, -0.83333, -1.66667, -1.50000, -1.33333, -1.16667, -1.00000, -0.83333, -0.66667, -0.50000, -0.33333, -0.16667],
          [0.00000, 0.00000, -0.75000, -1.50000, -2.25000, -2.00000, -1.75000, -1.50000, -1.25000, -1.00000, -0.75000, -0.50000, -0.25000],
          [0.00000, 0.00000, -0.66667, -1.33333, -2.00000, -2.66667, -2.33333, -2.00000, -1.66667, -1.33333, -1.00000, -0.66667, -0.33333],
          [0.00000, 0.00000, -0.58333, -1.16667, -1.75000, -2.33333, -2.91667, -2.50000, -2.08333, -1.66667, -1.25000, -0.83333, -0.41667],
          [0.00000, 0.00000, -0.50000, -1.00000, -1.50000, -2.00000, -2.50000, -3.00000, -2.50000, -2.00000, -1.50000, -1.00000, -0.50000],
          [0.00000, 0.00000, -0.41667, -0.83333, -1.25000, -1.66667, -2.08333, -2.50000, -2.91667, -2.33333, -1.75000, -1.16667, -0.58333],
          [0.00000, 0.00000, -0.33333, -0.66667, -1.00000, -1.33333, -1.66667, -2.00000, -2.33333, -2.66667, -2.00000, -1.33333, -0.66667],
          [0.00000, 0.00000, -0.25000, -0.50000, -0.75000, -1.00000, -1.25000, -1.50000, -1.75000, -2.00000, -2.25000, -1.50000, -0.75000],
          [0.00000, 0.00000, -0.16667, -0.33333, -0.50000, -0.66667, -0.83333, -1.00000, -1.16667, -1.33333, -1.50000, -1.66667, -0.83333],
          [0.00000, 0.00000, -0.08333, -0.16667, -0.25000, -0.33333, -0.41667, -0.50000, -0.58333, -0.66667, -0.75000, -0.83333, -0.91667]])

        L_sparse = sp.coo_matrix(L_full)
        L_data = L_sparse.data
        L_col = L_sparse.col.astype(np.int_)
        L_row = L_sparse.row.astype(np.int_)
        L_shape = L_sparse.shape[0]

        GXbarreb_sparse = sp.coo_matrix(GXbarrebr_full)
        GXbarreb_data = GXbarreb_sparse.data
        GXbarreb_col = GXbarreb_sparse.col.astype(np.int_)
        GXbarreb_row = GXbarreb_sparse.row.astype(np.int_)
        GXbarreb_shape = GXbarreb_sparse.shape[0]
        gam_expected = 0.055556
        beta_expected = 3.0

        gam, beta = cal_beta_gamma(L_data, L_row, L_col, L_shape,
                                   GXbarreb_data, GXbarreb_row, GXbarreb_col, GXbarreb_shape,
                                   Xbarre, Xbreve, a)
        self.assertAlmostEqual(gam, gam_expected, delta=1E-6)
        self.assertAlmostEqual(beta, beta_expected, delta=1E-6)


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(CalBetaGTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
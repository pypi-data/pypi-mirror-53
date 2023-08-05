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
from iw.reconstruction.operateur_reconstruction_one_step import operateur_reconstruction_one_step


class OperatorReconsTest(unittest.TestCase):

    def test_operateur_reconstruction_one_step(self):

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

        L_sparse = sp.coo_matrix(L_full)
        L = L_sparse.data
        L_col = L_sparse.col.astype(np.int_)
        L_row = L_sparse.row.astype(np.int_)
        L_shape = L_sparse.shape[0]

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

        GXbarreb_sparse = sp.coo_matrix(GXbarrebr_full)
        GXbarrebr = GXbarreb_sparse.data
        GXbarreb_col = GXbarreb_sparse.col.astype(np.int_)
        GXbarreb_row = GXbarreb_sparse.row.astype(np.int_)
        GXbarreb_shape = GXbarreb_sparse.shape[0]

        R = np.array([0, 1, 2])

        Lbarre_full = np.array([[-0.45, 0.25, 0.2],
                                [0.25, -0.39285714, 0.14285714],
                                [0.2, 0.14285714, -0.34285714]])

        Lbarre_sparse = sp.coo_matrix(Lbarre_full)
        Lbarre = Lbarre_sparse.data
        row_Lbarre = Lbarre_sparse.row.astype(np.int_)
        col_Lbarre = Lbarre_sparse.col.astype(np.int_)
        shape_Lbarre = Lbarre_sparse.shape[0]
        Xbarre = np.array(R, dtype=np.int_)

        qprime = 3.857142857142857

        (Rbarre, Rbarre_row, Rbarre_col,
         Rbarre_shape0, Rbarre_shape1,
         Rbreve, Rbreve_row, Rbreve_col,
         Rbreve_shape0, Rbreve_shape1) = operateur_reconstruction_one_step(
                                         L, L_row, L_col, L_shape,
                                         Lbarre, row_Lbarre,
                                         col_Lbarre, shape_Lbarre,
                                         GXbarrebr, GXbarreb_row,
                                         GXbarreb_col, GXbarreb_shape,
                                         Xbarre,
                                         qprime)
        self.assertEqual(Rbarre_shape0, Rbreve_shape0)
        self.assertEqual(Rbarre_shape1 + Rbreve_shape1, L_shape)
        self.assertEqual(Rbarre.size, Rbarre_row.size)
        self.assertEqual(Rbarre_col.size, Rbarre_row.size)
        self.assertEqual(Rbreve.size, Rbreve_row.size)
        self.assertEqual(Rbreve_row.size, Rbreve_col.size)

        self.assertTrue(Rbarre_col.dtype is np.dtype(np.int64))
        self.assertTrue(Rbarre_row.dtype is np.dtype(np.int64))
        self.assertTrue(Rbreve_col.dtype is np.dtype(np.int64))
        self.assertTrue(Rbreve_row.dtype is np.dtype(np.int64))


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(OperatorReconsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

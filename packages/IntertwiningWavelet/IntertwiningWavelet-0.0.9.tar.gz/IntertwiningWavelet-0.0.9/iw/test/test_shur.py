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
from iw.diaconis_fill.complementschur import complementschur


class ShurTest(unittest.TestCase):

    def test_schur(self):
        L_full = np.array(
         [[ -2.0 ,  1.0 ,  0 , 0  , 0  , 0 , 0  , 0  , 0  , 0  , 0  , 0 ,  0 ,  0  , 0 , 0],
          [  1.0 , -2.0 ,  1.0 , 0  , 0  , 0 , 0  , 0  , 0  , 0  , 0  , 0 ,  0 ,  0  , 0 , 0],
          [  0.0 ,  1.0 , -2.0 , 1.0  , 0  , 0 , 0  , 0  , 0  , 0  , 0  , 0 ,  0 ,  0  , 0 , 0],
          [  0.0 ,  0.0 ,  1.0 , -2.0 ,  1.0 , 0 , 0  , 0  , 0  , 0  , 0  , 0 ,  0 ,  0 ,  0 , 0],
          [  0.0 ,  0.0 ,  0.0 , 1.0  , -2.0 , 1.0 , 0  , 0  , 0  , 0  , 0  , 0 ,  0 ,  0 ,  0 , 0],
          [  0.0 ,  0.0 ,  0.0 , 0.0  , 1.0  ,-2.0 , 1.0  , 0  , 0  , 0  , 0  , 0 ,  0 ,  0 ,  0 , 0],
          [  0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 1.0 , -2.0 , 1.0  , 0  , 0  , 0  , 0 ,  0 ,  0 ,  0 , 0],
          [  0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 0.0 ,  1.0 , -2 , 1.0  , 0  , 0  , 0 ,  0 ,  0 ,  0 , 0],
          [  0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 0.0 ,  0.0 ,  1.0 ,-2.0  , 1.0  , 0  , 0 ,  0 ,  0 ,  0 , 0],
          [  0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 0.0 ,  0.0 ,  0.0 , 1.0  , -2.0 , 1.0  , 0 ,  0 ,  0 ,  0 , 0],
          [  0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 0.0 ,  0.0 ,  0.0 , 0.0  , 1.0  , -2.0 , 1.0 ,  0 ,  0 ,  0 , 0],
          [  0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 1.0  , -2.0,  1.0 ,  0 ,  0 , 0],
          [  0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 0.0  , 1.0 , -2.0 ,  1 ,  0 , 0],
          [  0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 0.0  , 0.0 ,  1.0 , -2.0 ,  1.0 , 0],
          [  0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 0.0  , 0.0 ,  0.0 ,  1.0 , -2.0 , 1],
          [  0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 0.0 ,  0.0 ,  0.0 , 0.0  , 0.0  , 0.0  , 0.0 ,  0.0 ,  0.0 ,  1.0 ,-2.0]])


        R = np.array( [0, 1,  2 ] , dtype=np.int_ )

        Xbarre = np.array(R, dtype=np.float64)
        Rc = np.array([ 3, 4, 5 ,6 ,7, 8, 9, 10 ,11 ,12 ,13, 14 ,15]  , dtype=np.int_)   
        Xbreve =  np.array(Rc, dtype=np.float64)

        GXbarrebr_expected_full = np.array(
             [[  -0.928571 , -0.857143 , -0.785714 , -0.714286 , -0.642857,  -0.571429 , -0.500000 , -0.428571 , -0.357143 , -0.285714 ,  -0.214286 , -0.142857 , -0.071429],
              [-0.857143  ,-1.714286  ,-1.571429  ,-1.428571 , -1.285714 , -1.142857 , -1.000000 , -0.857143 , -0.714286  ,-0.571429  ,-0.428571  ,-0.285714  ,-0.142857],
              [-0.785714  ,-1.571429 , -2.357143  ,-2.142857 , -1.928571  ,-1.714286  ,-1.500000 , -1.285714  ,-1.071429 , -0.857143  ,-0.642857,  -0.428571 , -0.214286],
              [ -0.714286 , -1.428571 , -2.142857 , -2.857143 , -2.571429 , -2.285714 , -2.000000 , -1.714286 , -1.428571 , -1.142857 , -0.857143,  -0.571429 , -0.285714],
              [ -0.642857  ,-1.285714,  -1.928571 , -2.571429 , -3.214286 , -2.857143 , -2.500000 , -2.142857 , -1.785714 , -1.428571 , -1.071429 , -0.714286 , -0.357143],
              [ -0.571429 , -1.142857 , -1.714286 , -2.285714 , -2.857143 , -3.428571 , -3.000000 , -2.571429 , -2.142857 , -1.714286 , -1.285714 , -0.857143 , -0.428571],
              [ -0.500000 , -1.000000 , -1.500000 , -2.000000 , -2.500000 , -3.000000 , -3.500000 , -3.000000 , -2.500000 , -2.000000 , -1.500000 , -1.000000 , -0.500000],
              [ -0.428571 , -0.857143 , -1.285714 , -1.714286 , -2.142857 , -2.571429 , -3.000000 , -3.428571 , -2.857143,  -2.285714 , -1.714286 , -1.142857 , -0.571429],
              [-0.357143  ,-0.714286  ,-1.071429 , -1.428571  ,-1.785714  ,-2.142857 , -2.500000 , -2.857143  ,-3.214286 , -2.571429 , -1.928571  ,-1.285714 , -0.642857],
              [-0.285714  ,-0.571429  ,-0.857143  ,-1.142857 , -1.428571  ,-1.714286 , -2.000000 , -2.285714  ,-2.571429 , -2.857143 ,-2.142857  ,-1.428571 , -0.714286],
              [-0.214286 , -0.428571 , -0.642857  ,-0.857143 , -1.071429 , -1.285714 , -1.500000 , -1.714286 , -1.928571 , -2.142857 ,-2.357143 , -1.571429 , -0.785714],
              [-0.142857 , -0.285714 , -0.428571 , -0.571429 , -0.714286  ,-0.857143 , -1.000000 , -1.142857  ,-1.285714 , -1.428571 , -1.571429 , -1.714286 , -0.857143],
              [ -0.071429 , -0.142857 , -0.214286 , -0.285714 , -0.357143 , -0.428571 , -0.500000 , -0.571429 , -0.642857 , -0.714286 , -0.785714 , -0.857143 , -0.928571]])

        L_sparse = sp.coo_matrix(L_full)
        L_data = L_sparse.data
        L_col = L_sparse.col.astype(np.int_) 
        L_row = L_sparse.row.astype(np.int_) 
        L_shape = L_sparse.shape[0]

        abarre_expected = 2

        Lbarre1d_full = np.array(
            [[ -1.00000 ,  1.00000  , 0.00000],
             [ 1.00000 , -2.00000  ,1.00000],
             [ 0.00000 ,  1.00000  , -1.0]])

#         GXbarreb_sparse = sp.coo_matrix(GXbarrebr_full)
#         GXbarreb_data_expected = GXbarreb_sparse.data
#         GXbarreb_col_expected = GXbarreb_sparse.col
#         GXbarreb_row_expected = GXbarreb_sparse.row
#         GXbarreb_shape_expected = GXbarreb_sparse.shape[0]

        Lbarre1d_sparse = sp.coo_matrix(Lbarre1d_full)
        Lbarre1d_data_expected = Lbarre1d_sparse.data
        Lbarre1d_col_expected = Lbarre1d_sparse.col
        Lbarre1d_row_expected = Lbarre1d_sparse.row
        Lbarre1d_shape_expected = Lbarre1d_sparse.shape[0]

        Lbarre1d, row1, col1, shape1, abarre, GXbarrebr, row2, col2, shape2 = complementschur(L_data, L_row,  L_col, L_shape,
                                                                                               R, Rc)

        GXbarrebr_sparse = sp.coo_matrix((GXbarrebr, (row2, col2)), shape=(shape2, shape2))
        GXbarrebr_full = GXbarrebr_sparse.todense()
        np.testing.assert_almost_equal(Lbarre1d.astype(np.float64), Lbarre1d_data_expected.astype(np.float64), 5)  
        np.testing.assert_array_equal(row1, Lbarre1d_row_expected)
        np.testing.assert_array_equal(col1, Lbarre1d_col_expected)

        # print(GXbarreb_data_expected)
        # np.testing.assert_array_equal(GXbarrebr.astype(np.float64), GXbarreb_data_expected.astype(np.float64), 5)
        np.testing.assert_almost_equal(GXbarrebr_full,  GXbarrebr_expected_full, 5)
#         np.testing.assert_array_equal(row2, GXbarrebr_expected_full )
#         np.testing.assert_array_equal(col2, GXbarreb_col_expected)

        self.assertTrue(shape1 == Lbarre1d_shape_expected)
        self.assertTrue(shape2 == GXbarrebr_expected_full.shape[0])


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(ShurTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
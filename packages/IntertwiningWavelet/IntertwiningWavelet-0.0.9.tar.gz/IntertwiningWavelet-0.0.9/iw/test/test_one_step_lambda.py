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
from iw.multiresolution.tab_one_step_Lambda import tab_one_step_Lambda


class OneStepLambdaTest(unittest.TestCase):

    def test_tab_one_step_lambda(self):
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
        n = 16
        L_sparse = sp.coo_matrix(L_full)
        L = L_sparse.data
        L_col = L_sparse.col.astype(np.int_)
        L_row = L_sparse.row.astype(np.int_)
        L_shape = L_sparse.shape[0]

        (Lambdabarre, row_lambdabr, col_lambdabr, shape0_lamdabr, shape1_lamdabr,
         Lambdabreve, row_lambdabv, col_lambdabv, shape0_lamdabv, shape1_lamdabv,
         qprime) = tab_one_step_Lambda(a,  L, L_row, L_col, L_shape, Xbarre, Xbreve, n)

        qprime_expected = 0.69231

        Lambdabarre_full_expected = np.array(
            [[ -50.3865,   99.4572, -143.8638,  182.8074, -214.4573,237.9519, -252.5664,  258.0971, -254.664 ,  242.7376,-223.0431,  196.5069, -164.1845,  127.2072,  -86.7385,43.9482],
          [  99.4572, -194.2503,  282.2646, -358.3211,  420.7594,
         -467.0237,  496.0491, -507.2304,  500.8348, -477.7071,
          439.2446, -387.2276,  323.7141, -250.923 ,  171.1554,
          -86.7385],
          [-143.8638,  282.2646, -408.7076,  520.2166, -610.8875,
          678.8565, -721.6877,  738.7867, -730.2735,  697.3417,
         -641.8916,  566.4518, -473.9662,  367.6623, -250.923 ,
          127.2072]])

        Lambdabreve_full_expected = np.array(
            [[ 182.8074, -358.3211,  520.2166, -662.274 ,  778.3137,
         -865.5515,  921.5941, -944.7309,  935.2936, -894.458 ,
          824.5489, -728.6302,  610.4   , -473.9662,  323.7141,
         -164.1845],
              [ -214.4573,   420.7594,  -610.8875,   778.3137,  -916.938 ,
          1021.0513, -1088.5946,  1118.1011, -1108.9153,  1062.5008,
          -981.1966,   868.4971,  -728.6302,   566.4518,  -387.2276,
           196.5069],
             [  237.9519,  -467.0237,   678.8565,  -865.5515,  1021.0513,
         -1139.9811,  1217.5583, -1252.7791,  1245.3083, -1195.6539,
          1106.449 ,  -981.1966,   824.5489,  -641.8916,   439.2446,
          -223.0431] ,
          [2.3912e-03, 6.4379e-03, 1.4942e-02, 3.3790e-02, 7.6031e-02, 1.7091e-01, -6.1589e-01, 1.7092e-01, 7.6053e-02, 3.3841e-02, 1.5057e-02, 6.6985e-03, 2.9770e-03, 1.3164e-03, 5.6720e-04, 2.1067e-04],
          [1.0640e-03, 2.8647e-03, 6.6486e-03, 1.5035e-02, 3.3831e-02, 7.6049e-02, 1.7092e-01, -6.1589e-01, 1.7092e-01, 7.6053e-02, 3.3840e-02, 1.5054e-02, 6.6903e-03, 2.9584e-03,  1.2747e-03, 4.7346e-04],
          [4.7346e-04, 1.2747e-03, 2.9584e-03, 6.6903e-03, 1.5054e-02, 3.3840e-02, 7.6053e-02, 1.7092e-01, -6.1589e-01, 1.7092e-01, 7.6049e-02, 3.3831e-02, 1.5035e-02, 6.6486e-03, 2.8647e-03, 1.0640e-03],
          [2.1067e-04, 5.6720e-04, 1.3164e-03, 2.9770e-03, 6.6985e-03, 1.5057e-02, 3.3841e-02, 7.6053e-02, 1.7092e-01, -6.1589e-01, 1.7091e-01, 7.6031e-02, 3.3790e-02, 1.4942e-02, 6.4379e-03, 2.3912e-03],
          [9.3740e-05, 2.5238e-04, 5.8573e-04, 1.3246e-03, 2.9805e-03, 6.6998e-03, 1.5057e-02, 3.3840e-02, 7.6049e-02, 1.7091e-01, -6.1591e-01, 1.7087e-01, 7.5937e-02 , 3.3579e-02, 1.4468e-02, 5.3739e-03],
          [4.1701e-05, 1.1227e-04, 2.6057e-04, 5.8927e-04, 1.3259e-03, 2.9805e-03, 6.6985e-03, 1.5054e-02, 3.3831e-02, 7.6031e-02, 1.7087e-01, -6.1601e-01, 1.7066e-01, 7.5463e-02, 3.2515e-02, 1.2077e-02],
          [1.8533e-05, 4.9897e-05, 1.1580e-04, 2.6188e-04, 5.8927e-04, 1.3246e-03, 2.9770e-03, 6.6903e-03, 1.5035e-02, 3.3790e-02, 7.5937e-02, 1.7066e-01, -6.1648e-01, 1.6959e-01, 7.3072e-02, 2.7141e-02],
          [8.1952e-06, 2.2064e-05, 5.1208e-05, 1.1580e-04, 2.6057e-04, 5.8573e-04, 1.3164e-03, 2.9584e-03, 6.6486e-03, 1.4942e-02, 3.3579e-02, 7.5463e-02, 1.6959e-01, -6.1887e-01, 1.6422e-01 , 6.0995e-02],
          [3.5311e-06, 9.5068e-06, 2.2064e-05, 4.9897e-05, 1.1227e-04, 2.5238e-04, 5.6720e-04, 1.2747e-03, 2.8647e-03, 6.4379e-03, 1.4468e-02, 3.2515e-02, 7.3072e-02, 1.6422e-01, -6.3095e-01, 1.3708e-01],
          [1.3115e-06, 3.5311e-06, 8.1952e-06, 1.8533e-05, 4.1701e-05, 9.3740e-05, 2.1067e-04, 4.7346e-04, 1.0640e-03, 2.3912e-03,  5.3739e-03, 1.2077e-02, 2.7141e-02, 6.0995e-02, 1.3708e-01, -6.9194e-01]])

        Lambdabarre_sp = sp.coo_matrix(
            (Lambdabarre, (row_lambdabr, col_lambdabr)), shape=(shape0_lamdabr, shape1_lamdabr))

        Lambdabarre_full = Lambdabarre_sp.todense()

        Lambdabreve_sp = sp.coo_matrix(
            (Lambdabreve, (row_lambdabv, col_lambdabv)), shape=(shape0_lamdabv, shape1_lamdabv))

        Lambdabreve_full = Lambdabreve_sp.todense()

        for i in range(Lambdabarre_full.shape[0]):
            np.testing.assert_almost_equal(Lambdabarre_full[[i], :], Lambdabarre_full_expected[[i], :], 4)
        for i in range(Lambdabarre_full.shape[0]):
            np.testing.assert_almost_equal(Lambdabreve_full[[i], :], Lambdabreve_full_expected[[i], :], 4)

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(OneStepLambdaTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

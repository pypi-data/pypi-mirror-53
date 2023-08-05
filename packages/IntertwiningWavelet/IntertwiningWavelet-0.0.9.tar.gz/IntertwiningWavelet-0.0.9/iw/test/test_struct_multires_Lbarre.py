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
from iw.graph_c import Graph_c
from iw.multiresolution.struct_multires_Lbarre import Tab_Struct_multires_Lbarre

from iw.multiresolution.struct_multires_Lbarre import Struct_M_ana_recons
from iw.multiresolution.struct_multires_Lbarre import Struct_multires_Lbarre

from iw.data.get_dataset_path import get_dataset_path
import numpy as np
from scipy import sparse as sp


class StructMultiResTest(unittest.TestCase):

    def test_init_Tab_Struct_multires_Lbarre(self):
        graph_file = get_dataset_path("tore1d16.g")
        option = {'-f': None, '-s': None, '-w': graph_file}
        graph = Graph_c(graph_file)
        graph._cal_Laplacien()
        num_dict = graph._nativeNum_function()
        mu = graph.mu_initial
        a = 1.5
        mod = 'step'
        n = num_dict['n']
        steps = n//4
        m = 1
        theta = 4.0
        tab = Tab_Struct_multires_Lbarre(graph, a, mu, n, mod, m, steps, theta)
        self.assertGreaterEqual(steps, tab.steps)
        # self.assertIsInstance(tab.Struct_Mres_gr, Struct_multires_Lbarre[:])

    def test_init_Struct_M_ana_recons(self):

        Lambdabarre_full = np.array(
            [[-2.00000, 0.00000, 0.00000, 4.5],
             [1.00000, -2.00000, 1.00000, 8.6],
             [0.00000, 1.00000, -1.07143, 10.2]])
        Lambdabarre_sp = sp.coo_matrix(Lambdabarre_full)
        Lambdabarre = Lambdabarre_sp.data
        rowla = np.array(Lambdabarre_sp.row, dtype=np.int_)
        colla = np.array(Lambdabarre_sp.col, dtype=np.int_)
        shape0la = Lambdabarre_sp.shape[0]
        shape1la = Lambdabarre_sp.shape[1]

        Lambdabreve_full = np.array(
            [[-2.00000, 1.00000],
             [0.0, 1.0],
             [4.5, 6.5],
             [0.0, 6.5],
             [0.0, 6.5]])
        Lambdabreve_sp = sp.coo_matrix(Lambdabreve_full)
        Lambdabreve = Lambdabreve_sp.data
        rowlb = np.array(Lambdabreve_sp.row, dtype=np.int_)
        collb = np.array(Lambdabreve_sp.col, dtype=np.int_)
        shape0lb = Lambdabreve_sp.shape[0]
        shape1lb = Lambdabreve_sp.shape[1]

        Reconsbarre_full = np.array(
           [[-2.00000, 18.00000, 0.00000, 4.5],
            [1.00000, -2.00000, 1.00000, 8.6],
            [17.00000, 1.00000, -1.07143, 10.2]])

        Reconsbarre_sp = sp.coo_matrix(Reconsbarre_full)
        Reconsbarre = Reconsbarre_sp.data
        rowlra = np.array(Reconsbarre_sp.row, dtype=np.int_)
        collra = np.array(Reconsbarre_sp.col, dtype=np.int_)
        shape0lra = Reconsbarre_sp.shape[0]
        shape1lra = Reconsbarre_sp.shape[1]

        Reconsbreve_full = np.array(
            [[-15.00000, 1.00000],
             [16.0, 1.0],
             [4.5, 6.5],
             [20.0, 6.5],
             [18.0, 6.5]])
        Reconsbreve_sp = sp.coo_matrix(Reconsbreve_full)
        Reconsbreve = Reconsbreve_sp.data
        rowlrb = np.array(Reconsbreve_sp.row, dtype=np.int_)
        collrb = np.array(Reconsbreve_sp.col, dtype=np.int_)
        shape0lrb = Reconsbreve_sp.shape[0]
        shape1lrb = Reconsbreve_sp.shape[1]

        st_Lambda = Struct_M_ana_recons(
            Lambdabarre, rowla, colla, shape0la, shape1la,
            Lambdabreve, rowlb, collb, shape0lb, shape1lb,
            Reconsbarre, rowlra, collra, shape0lra, shape1lra,
            Reconsbreve, rowlrb, collrb, shape0lrb, shape1lrb)

        self.assertEqual(st_Lambda.shape0Lambdabarre, shape0la)
        self.assertEqual(st_Lambda.shape1Lambdabarre, shape1la)
        np.testing.assert_equal(st_Lambda.colLambdabarre, colla)
        np.testing.assert_equal(st_Lambda.rowLambdabarre, rowla)
        np.testing.assert_equal(st_Lambda.Lambdabarre, Lambdabarre)

        self.assertEqual(st_Lambda.shape0Lambdabreve, shape0lb)
        self.assertEqual(st_Lambda.shape1Lambdabreve, shape1lb)
        np.testing.assert_equal(st_Lambda.rowLambdabreve, rowlb)
        np.testing.assert_equal(st_Lambda.colLambdabreve, collb)
        np.testing.assert_equal(st_Lambda.Lambdabreve, Lambdabreve)

        self.assertEqual(st_Lambda.Recons_shape0_barre, shape0lra)
        self.assertEqual(st_Lambda.Recons_shape1_barre, shape1lra)
        np.testing.assert_equal(st_Lambda.Recons_col_barre, collra)
        np.testing.assert_equal(st_Lambda.Recons_row_barre, rowlra)
        np.testing.assert_equal(st_Lambda.Reconsbarre,  Reconsbarre)

        self.assertEqual(st_Lambda.Recons_shape0_breve, shape0lrb)
        self.assertEqual(st_Lambda.Recons_shape1_breve, shape1lrb)
        np.testing.assert_equal(st_Lambda.Recons_row_breve, rowlrb)
        np.testing.assert_equal(st_Lambda.Recons_col_breve, collrb)
        np.testing.assert_equal(st_Lambda.Reconsbreve, Reconsbreve)

    def test_init_Struct_multires_Lbarre(self):
        Lbarre1d_full = np.array(
            [[-2.00000, 1.00000, 0.00000],
             [1.00000, -2.00000, 1.00000],
             [0.00000, 1.00000, -1.07143]])

        Lbarre_sp = sp.coo_matrix(Lbarre1d_full)
        Lbarre = Lbarre_sp.data
        rowlb = np.array(Lbarre_sp.row, dtype=np.int_)
        collb = np.array(Lbarre_sp.col, dtype=np.int_)
        shapelb = Lbarre_sp.shape[0]

        Lbarres_full = np.array(
            [[-4.000, 6.000, 2.000],
             [0.000, -2.000, 0.000],
             [1.000, -3.000, -1.071]])

        Lbarres_sp = sp.coo_matrix(Lbarres_full)
        Lbarres = Lbarres_sp.data
        rowlbs = np.array(Lbarres_sp.row, dtype=np.int_)
        collbs = np.array(Lbarres_sp.col, dtype=np.int_)
        shapelbs = Lbarres_sp.shape[0]
        alphabar = 1.5

        mu = np.array([1.0, 1.0, 1.0])
        Xbarre = np.array([1, 2, 3], dtype=np.int_)

        gamma = 0.055556
        beta = 3
        q = 10.000
        qprime = 0.1

        st_Lbarre = Struct_multires_Lbarre(Lbarre, rowlb, collb, shapelb,
                                           Lbarres, rowlbs, collbs, shapelbs,
                                           alphabar, mu,  Xbarre, gamma, beta,
                                           q, qprime)

        self.assertEqual(st_Lbarre.q, q)
        self.assertEqual(st_Lbarre.qprime, qprime)
        self.assertEqual(st_Lbarre.beta, beta)
        self.assertEqual(st_Lbarre.gamma, gamma)
        np.testing.assert_equal(st_Lbarre.Xbarre, Xbarre)
        np.testing.assert_equal(st_Lbarre.mubarre, mu)

        self.assertEqual(st_Lbarre.shapeLbarre, shapelb)
        self.assertEqual(st_Lbarre.shapeLbarres, shapelbs)

        np.testing.assert_equal(st_Lbarre.colLbarre, collb)
        np.testing.assert_equal(st_Lbarre.rowLbarre, rowlb)
        np.testing.assert_equal(st_Lbarre.Lbarre, Lbarre)

        np.testing.assert_equal(st_Lbarre.rowLbarres, rowlbs)
        np.testing.assert_equal(st_Lbarre.colLbarres, collbs)
        np.testing.assert_equal(st_Lbarre.Lbarres, Lbarres)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(StructMultiResTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()

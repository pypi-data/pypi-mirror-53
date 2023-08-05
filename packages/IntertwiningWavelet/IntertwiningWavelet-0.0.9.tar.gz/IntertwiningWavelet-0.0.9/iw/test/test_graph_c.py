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

from iw.data.get_dataset_path import get_dataset_path
import numpy as np
from scipy import sparse as sp


class UnitaryTest(unittest.TestCase):

    def test_init_graph(self):
        # print("test_init_graph")
        graph_file = get_dataset_path("tore1d16.g")
        option = {'-f': None, '-s': None, '-w': graph_file}
        gr = Graph_c(graph_file)
        self.assertTrue(gr.option_forest == option)
        nbr = 4
        self.assertTrue(gr.nbr_entry == nbr)

        for k in gr.option_forest.keys():
            e = k.encode('utf-8')
            self.assertTrue(e in gr.entry)

        self.assertTrue(gr.reversible)
        num_dict = gr._nativeNum_function()

        self.assertTrue(num_dict['n'] == 16)
        self.assertTrue(num_dict['na'] == 64)
        self.assertTrue(num_dict['ttm'] == 4)
        # self.assertTrue(num_dict['tu']==0)
        # self.assertTrue(num_dict['a']==139812937050928)

        # self.assertTrue(num_dict['f']==1)
        self.assertTrue(num_dict['q'] == -1)
        self.assertTrue(num_dict['tmp_inv'] == 0)
        self.assertTrue(num_dict['Z'] == 16)

    def test_cal_Laplacien(self):
        # print("test_cal_Laplacien")
        graph_file = get_dataset_path("tore1d16.g")
        # option = {'-f':None , '-q':None, '-l':None , '-L':None, '-s':None,'-f': None,'-k': None, '-w':  graph_file}

        Laplacien_expected = np.array(
            [-2.0, 1.0, 1.0, 1.0, -2.0, 1.0, 1.0, -2.0, 1.0,
             1.0, -2.0, 1.0, 1.0, -2.0, 1.0, 1.0, -2.0, 1.0,
             1.0, -2.0, 1.0, 1.0, -2.0, 1.0, 1.0, -2.0, 1.0,
             1.0, -2.0, 1.0, 1.0, -2.0, 1.0, 1.0, -2.0, 1.0,
             1.0, -2.0, 1.0, 1.0, -2.0, 1.0, 1.0, -2.0, 1.0,
             1.0, 1.0, -2.0])
        row_expected = np.array(
            [0, 1, 15, 0, 1, 2, 1, 2, 3, 2, 3, 4, 3, 4, 5, 4, 5, 6,
             5, 6, 7, 6, 7, 8, 7, 8, 9, 8, 9, 10, 9, 10, 11, 10, 11,
             12, 11, 12, 13,
             12, 13, 14, 13, 14, 15, 0, 14, 15])
        col_expected = np.array(
            [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6,
             6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11,
             12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15])

        L_expected_sp = sp.coo_matrix(
            (Laplacien_expected, (row_expected, col_expected)),
            shape=(16, 16))
        L_expected_dense = L_expected_sp.todense()

        gr = Graph_c(graph_file)
        gr._cal_Laplacien()

        data = gr.Laplacien
        row = gr.row
        col = gr.col
        shape = gr.shape

        Laplacien_sp = sp.coo_matrix(
            (data, (row, col)), shape=(shape, shape))
        Laplacien_dense = Laplacien_sp.todense()
        self.assertTrue((Laplacien_dense == L_expected_dense).all())

    def test_cal_C_struct(self):
        # print("test_cal_C_struct")
        graph_file = get_dataset_path("tore1d16.g")

        gr = Graph_c(graph_file)
        gr._cal_Laplacien()
        self.assertTrue(gr.Laplacien[1] == 1)
        gr.Laplacien[1] = 3.0
        gr._cal_C_struct()
        num_dict = gr._nativeNum_function()
        gr._cal_Laplacien()
        self.assertTrue(gr.Laplacien[1] == 3)

    def test_initialisation_grezza_like(self):
        # print("test_initialisation_grezza_like")
        graph_file = get_dataset_path("tore1d16.g")

        gr = Graph_c(graph_file)

        gr._cal_Laplacien()

        gr._initialisation_grezza_like()

        num_dict = gr._nativeNum_function()

        param_dict = gr._nativeParam_function()

        self.assertTrue(num_dict['q'] == 1.0 / 512.0)
        self.assertTrue(param_dict['L'] == 512)
        self.assertTrue(param_dict['l'] == 512)
        self.assertTrue(param_dict['m'] == 0)
        self.assertTrue(param_dict['e'] == 2.0)
        self.assertTrue(param_dict['immagini'] == 12)
        self.assertTrue(param_dict['pausa'] == 0)
        self.assertTrue(param_dict['verboso'] == 1)
        self.assertTrue(param_dict['da_file'] == 0)
        self.assertTrue(param_dict['z'] == -1.0)
        self.assertTrue(param_dict['X'] == 0)
        self.assertTrue(param_dict['stampa_foresta'] == 0)
        self.assertTrue(param_dict['flag_outputfile'] == 0)
        self.assertTrue(param_dict['outputfilename'] == b"./output.txt")
        self.assertTrue(param_dict['flag_outputErrorfile'] == 0)
        self.assertTrue(param_dict['outputErrorfilename'] == b"./outputerrorfile.txt")

        self.assertTrue(param_dict['fr'] == 0)
        self.assertTrue(param_dict['q_min'] == 0)
        self.assertTrue(param_dict['scrivere'] == 0)

    def test_initialise_sample_root(self):
        # print("test_initialise_sample_root")
        graph_file = get_dataset_path("tore1d16.g")

        gr = Graph_c(graph_file)
        gr._cal_Laplacien()
        gr._initialise_sample_root(0.001)
        self.assertTrue(gr.option_forest['-w'] == graph_file)
        self.assertTrue(gr.option_forest['-q'] == 0.001)
        num_dict = gr._nativeNum_function()
        param_dict = gr._nativeParam_function()

        self.assertTrue(num_dict['q'] == 0.001)

        self.assertTrue(param_dict['da_file'] == 1)
        self.assertTrue(param_dict['grafo'] == graph_file)

    def test_sample_root(self):
        # print("test_sample_root")
        graph_file = get_dataset_path("tore1d16.g")
        gr = Graph_c(graph_file)
        gr._cal_Laplacien()
        R, newRc, k = gr.sample_root_q(0.001, 16)
        self.assertTrue(R.shape[0] == k)
        self.assertFalse(np.in1d(R, newRc).all())
        self.assertFalse(np.in1d(newRc, R).all())
        test = np.append(R, newRc)
        test = np.sort(test)
        self.assertTrue(np.in1d(test, np.arange(test.size)).any())

    def test_initialise_choixm_q(self):
        graph_file = get_dataset_path("tore1d16.g")

        gr = Graph_c(graph_file)
        gr._cal_Laplacien()
        n = gr._initialise_choixm_q(0.001, 0.1)
        num_dict = gr._nativeNum_function()
        param_dict = gr._nativeParam_function()
        self.assertTrue(num_dict['n'] == 16)
        self.assertTrue(gr.option_forest['-w'] == param_dict['grafo'])
        self.assertTrue(param_dict['da_file'] == 1)
        self.assertTrue(param_dict['fr'] == 1)
        self.assertTrue(param_dict['m'] == 0)

        self.assertTrue(gr.option_forest['-k'] == 0.001)
        self.assertTrue(param_dict['q_min'] == 0.001)
        self.assertTrue(gr.option_forest['-q'] == 0.1)
        self.assertTrue(num_dict['q'] == 0.1)

    def test_choixq_m(self):
        graph_file = get_dataset_path("tore1d16.g")

        gr = Graph_c(graph_file) # , opt=None
        gr._cal_Laplacien()
        timebc, taf, itbf, tasurtbf, qc, nRR = gr.choixq_m(0.0125, 0.1, 1, 1.5, 16)

        self.assertEqual(timebc.size, nRR.size)
        self.assertEqual(itbf.size, tasurtbf.size)
        self.assertEqual(taf.size, itbf.size)
        self.assertEqual(tasurtbf.size, tasurtbf.size)
        self.assertEqual(timebc.size, tasurtbf.size)

    def test_tab_one_step_Lbarre_sparse(self):

        graph_file = get_dataset_path("tore1d16.g")
        graph = Graph_c(graph_file)
        graph._cal_Laplacien()
        num_dict = graph._nativeNum_function()
        mu = graph.mu_initial
        L = graph.Laplacien
        row = graph.row
        col = graph.col

        shape = graph.shape
        n = num_dict['n']
        a = 1.5
        steps = n // 4
        # steps = 0
        theta = 0.1
        (Lbarres, row_brs, col_brs, shape_brs,
         Lbarre, row1, col1, shape1,
         mubarre, Xbarre, Xbreve, alphabar, gam, beta,
         GXbarrebr, row2, col2, shape2, q, qprime,
         Lambdabarre, row_lambdabr, col_lambdabr,
         shape0_lamdabr, shape1_lamdabr,
         Lambdabreve, row_lambdabv, col_lambdabv,
         shape0_lamdabv, shape1_lamdabv) = graph.tab_one_step_Lbarre_sparse(
            L, row, col, shape,
            a, mu, steps, n, theta)

        self.assertEqual(Lbarres.size, row_brs.size)
        self.assertEqual(col_brs.size, row_brs.size)
        self.assertEqual(Lbarre.size, row1.size)
        self.assertEqual(col1.size, row1.size)
        self.assertEqual(GXbarrebr.size, row2.size)
        self.assertEqual(col2.size, row2.size)
        self.assertEqual(Lambdabarre.size, row_lambdabr.size)
        self.assertEqual(col_lambdabr.size, row_lambdabr.size)
        self.assertEqual(Lambdabreve.size, row_lambdabv.size)
        self.assertEqual(col_lambdabv.size, row_lambdabv.size)
        self.assertEqual(shape0_lamdabv + shape0_lamdabr, n)
        self.assertEqual(shape1_lamdabr, shape1_lamdabv)
        self.assertEqual(Xbarre.size, shape0_lamdabr)
        self.assertEqual(Xbreve.size, shape0_lamdabv)
        self.assertEqual(shape1+shape2, n)
        Lbarre_sp = sp.coo_matrix((Lbarre, (row1, col1)), shape=(shape1, shape1))
        Lbarre_full = Lbarre_sp.toarray()
        # print(qprime)


if __name__ == '__main__':
    unittest.main()
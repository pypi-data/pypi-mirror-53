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

from iw.data.get_dataset_path import get_dataset_path
import numpy as np
from scipy import sparse as sp
from iw.graph_c import Graph_c
from iw.multiresolution.struct_multires_Lbarre import Tab_Struct_multires_Lbarre
from iw.reconstruction.tab_reconstruction_multires import tab_reconstruction_multires
from iw.reconstruction.tab_reconstruction_multires import _cal_f
from iw.reconstruction.tab_compute_multires_coeffs_sparse import tab_compute_multires_coeffs_sparse


class TabReconsTest(unittest.TestCase):

    def test_tab_recons_multires(self):
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

        tab_Multires = Tab_Struct_multires_Lbarre(graph, a, mu, n, mod, m, steps, theta)
        f = np.linspace(0, 3, n)
        coeffs, suite_taille = tab_compute_multires_coeffs_sparse(
            f,
            tab_Multires.Struct_Mana_re,
            tab_Multires.steps)
        steps_f = tab_Multires.steps
        frecons = tab_reconstruction_multires(coeffs,
                                              tab_Multires.Struct_Mana_re,
                                              steps_f)
        self.assertEqual(frecons.size, coeffs.size)

        # self.assertEqual(f_expected.size, coeffs.size)
        # np.testing.assert_almost_equal(f, frecons) # can't be testing random

    def test_cal_f(self):
        # f =  _cal_f(coeffs, Struct_Mana_re, int step)
        pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TabReconsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    # unittest.main()

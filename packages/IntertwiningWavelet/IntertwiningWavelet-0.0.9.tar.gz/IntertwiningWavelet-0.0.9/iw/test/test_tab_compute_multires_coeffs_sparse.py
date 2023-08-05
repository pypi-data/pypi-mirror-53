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
from iw.reconstruction.tab_compute_multires_coeffs_sparse import tab_compute_multires_coeffs_sparse
from iw.multiresolution.struct_multires_Lbarre import Tab_Struct_multires_Lbarre, Struct_M_ana_recons


class TabComputTest(unittest.TestCase):

    def test_tab_compute_multires_coeffs_sparse(self):

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

        self.assertEqual(coeffs.size, suite_taille.sum())
        self.assertEqual(coeffs.size, f.size)
        self.assertEqual(mu.size, coeffs.size)
        self.assertGreaterEqual(steps, tab_Multires.steps)


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TabComputTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

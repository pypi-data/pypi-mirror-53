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
from iw.intertwining_wavelet import IntertwiningWavelet
from iw.graph_c import Graph_c

from iw.data.get_dataset_path import get_dataset_path
from iw.multiresolution.struct_multires_Lbarre import Struct_M_ana_recons
from iw.multiresolution.struct_multires_Lbarre import Struct_multires_Lbarre

class IntertwiningTest(unittest.TestCase):

    def test_init_intertwining_wavelet(self):
        graph_file = get_dataset_path("tore1d16.g")
        opt = None
        # gr = Graph_c(graph_file, opt)
        pyram = IntertwiningWavelet(graph_file)
        self.assertTrue(pyram.pretreatment)
        self.assertEquals(16, pyram.mu_initial.size)
        mu_expected = np.ones(16, dtype=np.double)
        np.testing.assert_array_almost_equal(mu_expected, pyram.mu_initial, 6)
        self.assertTrue(pyram.graph.reversible)

    def test_process_analysis(self):
        graph_file = get_dataset_path("tore1d16.g")
        pyram = IntertwiningWavelet(graph_file)
        pyram.process_analysis(mod='step')
        tab = pyram.tab_Multires
        self.assertGreaterEqual(10, tab.steps)
        self.assertEqual(tab.Struct_Mres_gr.size, tab.steps)
        self.assertEqual(tab.Struct_Mana_re.size, tab.steps)
        self.assertIsInstance(tab.Struct_Mres_gr[0], Struct_multires_Lbarre)
        self.assertIsInstance(tab.Struct_Mana_re[0], Struct_M_ana_recons)

    def test_process_reconstruction(self):
        graph_file = get_dataset_path("tore1d16.g")
        pyram = IntertwiningWavelet(graph_file)
        pyram.process_analysis(mod='step')

        with self.assertRaises(NameError):
            pyram.process_reconstruction_signal()

        signal = np.ones((1, 16), dtype=np.double)
        signal[:, 8: 16-1] = signal[:, 8:16-1] - 2
        # sign = pyram.process_reconstruction_signal(signal)
        coef_return = pyram.process_coefficients(signal)
        #print(np.asarray(pyram.following_size))
        coef = pyram.coeffs
        # sign = pyram.process_signal(coef_return)
        sign = pyram.process_reconstruction_signal(signal)
        #np.testing.assert_array_almost_equal(coef , coef_return, 6)

        np.testing.assert_array_almost_equal(signal[0,:], sign[0,:], 6)


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(IntertwiningTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
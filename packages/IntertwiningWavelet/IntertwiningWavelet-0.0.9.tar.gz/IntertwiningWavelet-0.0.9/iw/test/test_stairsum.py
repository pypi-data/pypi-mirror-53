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
from iw.function_fab.stairsum import stairsum


class StairsumTest(unittest.TestCase):

    def test_stairsum(self):
        q = np.array([10.000, 20.566, 57.518])
        R = np.array([1., 2., 3.])
        qq = np.array([10.000,  20.566, 57.518])
        RR = np.array([15., 14., 13.])
        qs, Rs = stairsum(q, R, qq, RR)
        qsexpected = np.array([10.000, 20.566, 57.518])
        Rsexpected = np.array([16, 16, 16])
        np.testing.assert_almost_equal(qsexpected, qs)
        np.testing.assert_equal(Rsexpected, Rs)


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(StairsumTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
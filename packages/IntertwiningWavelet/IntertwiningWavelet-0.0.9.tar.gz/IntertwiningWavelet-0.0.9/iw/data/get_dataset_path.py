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
#
"""Module to get the absolute path of a reference dataset for tests

.. moduleauthor:: Denis Arrivault
"""

from __future__ import print_function, division

import os


def get_dataset_path(filename):
    """Return the absolute path of a reference dataset for tests

    - Input parameter:

    :param str filename: File name of the file containing reference data
        for tests (which must be in ``skgilearn/tests/datasets/``)

    - Output parameters:

    :returns: The absolute path where the file with name **filename** is stored
    :rtype: str

    """

    datasets_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(datasets_path, filename)

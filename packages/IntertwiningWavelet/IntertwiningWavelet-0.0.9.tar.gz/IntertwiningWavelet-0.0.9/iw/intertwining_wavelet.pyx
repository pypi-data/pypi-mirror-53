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
import cython
import numpy as np
from numpy.testing.utils import suppress_warnings
cimport numpy as np
cimport iw.graph_c
from iw.graph_c cimport Graph_c
cimport iw.multiresolution.struct_multires_Lbarre
from iw.multiresolution.struct_multires_Lbarre cimport Tab_Struct_multires_Lbarre
cimport iw.reconstruction.tab_reconstruction_multires
from iw.reconstruction.tab_reconstruction_multires cimport tab_reconstruction_multires
cimport iw.reconstruction.tab_compute_multires_coeffs_sparse
from  iw.reconstruction.tab_compute_multires_coeffs_sparse cimport tab_compute_multires_coeffs_sparse
import scipy.sparse as sp


cdef class IntertwiningWavelet:
    """ Define an automaton with parameters

    :Example::

    >>> from iw.data.get_dataset_path import get_dataset_path
    >>> from iw.intertwining_wavelet import IntertwiningWavelet
    >>> graph_file = get_dataset_path("tore1d16.g")
    >>> iw = IntertwiningWavelet(graph_file)
    >>> iw.mu_initial.size
    >>> 16
    >>> iw.pretreatment
    >>> True
    >>> iw.process_analysis(mod='step')
    >>> tab = iw.tab_Multires
    >>> iw.process_analysis_flag
    >>> True
    >>> iw.process_reconstruction(signal)

    - Input::

    :param str graph_file: name of the graph file
    :param signals: array of signals
    :type signals: 2d array of double can be also one vector
    :param int nbr_signals: number of signals
    :param list transition: the transitions tables
    :param boolean pretreatment: True if pretreatement  performed

    - Attributes::

    :ivar signals: array of input signal for reconstructions
    :type signals: 2d array
    :ivar  bool pretreatment: True if pretreatment has been performed
    :ivar int nbr_signals: number of signals
    :ivar graph:  current graph :class:`iw.gaph_c.Graph_c`
    :type graph: :class:`iw.gaph_c.Graph_c`
    :ivar tab_Multires: structure of :class:`iw.multiresolution.struct_multires_Lbarre.Tab_Struct_multires_Lbarre`
    :type tab_Multires: Tab_Struct_multires_Lbarre
    :ivar mu_initial: array of value of initial :math:`\\mu`
    :type mu_initial: array
    :ivar reconstructed_s: array of reconstructed signals
    :type reconstructed_s: 2d array
    :ivar coeffs: arrays of coefficients
    :type coeffs: 2d array
    :ivar  following_size: array of all sizes
    :type following_size: 1d int array
    :ivar double a: value varaible a (max of trac of laplacien)
    :ivar str graph_file_initial: name of initial graph for decomposition
    :ivar bool process_analysis_flag: Tru if process_analysys has been performed

    """
    def __init__(self, graph_file, mu=None,  signals=None):
        if signals is not None:
            self.nbr_signals = signals.shape[0]
            self.signals = signals
        else:
            self.signals = None
        self.pretreatment = False
        if mu is not None:
            self.mu_initial = mu
        else:
            self.mu_initial = None
        try:
            self.graph = Graph_c(graph_file)
            self.graph_file_initial = graph_file
        except Exception:
            raise IOError("Graph can not be loaden")
        self._calc_a()
        if not self.pretreatment:
            self.process_pretreatment()
        self.process_analysis_flag = False

    def __getstate__(self):
        return (self.signals,  self.pretreatment, self.nbr_signals, self.graph,
         self.tab_Multires, self.mu_initial, self.reconstructed_s, self.coeffs,
         self.following_size, self.a, self.graph_file_initial,self. process_analysis_flag)

    def __setstate__(self, state):
        (signals,  pretreatment, nbr_signals, graph,
         tab_Multires, mu_initial, reconstructed_s, coeffs,
         following_size, a, graph_file_initial, process_analysis_flag) = state
        self.signals = signals
        self.pretreatment = pretreatment
        self.nbr_signals = nbr_signals
        self.graph = graph
        self.tab_Multires = tab_Multires
        self.mu_initial = mu_initial
        self.reconstructed_s = reconstructed_s
        self.coeffs = coeffs
        self.following_size = following_size
        self.a = a
        self.graph_file_initial = graph_file_initial
        self.process_analysis_flag = process_analysis_flag


    def process_pretreatment(self):
        """ process_pretreatment function called by init

        """
        if self.graph.reversible:
            print(""""The graph is reversible the pyramide algorithm....
                   can proceed""")
            if self.mu_initial is None:
                self._cal_mu()
        else:
            print(""" The graph is not reversible, the Pyramide algorithm,
                  is not optimum ...""")
        self.pretreatment = True

    def _cal_mu(self):
        # mu =  self.graph.mu_initial
        # return mu
#         cdef int i
#         cdef np.ndarray mu
#         mu = np.zeros(self.graph._nativeNum.n)
#         for i in range(self.graph._nativeNum.n):
#             mu[i] = self.graph._nativePunto[i].pot
        self.mu_initial = self.graph.mu_initial
        return self.mu_initial

    def _calc_a(self):
        """Compute the initial a from the first Laplacien """
        L = self.graph.Laplacien
        row = self.graph.row
        col = self.graph.col
        shape = self.graph.shape
        sL = sp.csr_matrix((L, (row, col)),
                           shape=(shape, shape))
        self.a = np.max(np.abs(sL.diagonal()))

    def process_analysis(self, mod='step', steps=10, m=0, theta=4.0):
        """process_analysis launch multiresolution analysis

        - Inputs::

        :param mod: (default value = 'step') define the mod of the
                  multiresolution analysis of multiscale calculations:

                    * 'step' determine the number of steps for decomposition

                    * 'card' determine the minimum cardinal of graph m
        :type mod: string
        :param int steps: (default value = 10) number of steps for
                        multiresolution
        :param int m: (default value = None) number of minimum cardinality

        :param double theta: (default value = 4.0) parameter which determines the level
                           of sparsification

        """
        #:param double a: (default value = 2.0) parameter which determines
        #               optimum value of q to sample the vertices of the new graph
        if self.process_analysis_flag:
            try:
                self.graph = Graph_c(self.graph_file_initial)
                self.mu_initial = self.graph.mu_initial
            except Exception:
                raise IOError("Graph can not be loaden")
        self._multiresolution(mod=mod, m=m, steps=steps, theta=theta)
        self.process_analysis_flag = True

    def _multiresolution(self, mod, m, steps, theta):
        # a = 2
        # m = 10
        n = self.graph._nativeNum.n

        L = self.graph.Laplacien
        row = self.graph.row
        col = self.graph.col
        shape = self.graph.shape
        a = self.a

        nom_graphe = self.graph.option_forest['-w']

        tab_Multires = Tab_Struct_multires_Lbarre(self.graph, a,
                                                  self.mu_initial, n,
                                                  mod, m, steps,
                                                  theta)

        self.tab_Multires = tab_Multires

    def process_coefficients(self, signals=None):
        """compute multiresolution coefficients of the signals

        - Input

        :param signals: array of signals to reconstruct
        :type signals: 2d array of double can have only one vector

        - Output

        :returns: coefficients of the multiresolution decomposition
        :rtype: coefficients  2d array of double can be also one vector

        """
        if signals is None and self.signals is None:
            raise NameError("Reconstruction needs signals")
        elif signals is not None:
            self.signals = signals
        return np.asarray(self._reconstruction(coeff_compute=True, signal_compute=False))

    def _reconstruction(self, coeff_compute=True, signal_compute=True):
        try:
            Struct_Mana = self.tab_Multires.Struct_Mana_re
        except Exception:
            raise NameError("process analysis must be perform first")
        if self.signals.ndim == 1:
            self.nbr_signals = 1
            f = self.signals
        else:
            f = self.signals[0, :]
            self.nbr_signals = self.signals.shape[0]
        if signal_compute and not coeff_compute:
            nbr_loop = self.coeffs.shape[0]
        if coeff_compute:
            nbr_loop = self.nbr_signals
           
        for isignal in range(nbr_loop):
            if coeff_compute:
                f = self.signals[isignal, :]
                coeffs, suite_taille = tab_compute_multires_coeffs_sparse(
                                     f,
                                     Struct_Mana,
                                     self.tab_Multires.steps)
                if isignal == 0:
                    self.coeffs = np.asarray(coeffs).reshape(1, coeffs.shape[0])
                    self.following_size = np.asarray(suite_taille)
                else:
                    self.coeffs = np.vstack((self.coeffs, np.asarray(coeffs)))
            if signal_compute:
                coeffs = self.coeffs[isignal, :]   
                g = tab_reconstruction_multires(coeffs, Struct_Mana,
                                                self.tab_Multires.steps)
                if isignal == 0:
                    self.reconstructed_s = np.asarray(g).reshape(1, g.shape[0])
                else:
                    self.reconstructed_s = np.vstack((self.reconstructed_s, np.asarray(g)))
        if not signal_compute:
            return np.asarray(self.coeffs)

        return np.asarray(self.reconstructed_s)

    def process_reconstruction_signal(self, signals=None):
        """process reconstruction of the signals given signals (check the reliability of the IW Toolbox)

        - Input

        :param signals: array of signals to reconstruct
        :type signals: 2d array of double can have only one vector

        - Output

        :returns: reconstructed_signals
        :rtype: reconstructed_signals  2d array of double can be also one vector

        """
        if signals is None and self.signals is None:
            raise NameError("Reconstruction needs signals")
        elif signals is not None:
            self.signals = signals
        return self._reconstruction(coeff_compute=True, signal_compute=True)

    def process_signal(self, coeffs):
        """process reconstruction given coefficients 

        - Input

        :param coeffs: array of wavelet coefficients
        :type coeffs: 2d array of double, can only have one line in the case of one vector.

        - Output

        :returns: reconstructed_signals
        :rtype: reconstructed_signals 2d array of double, can only have one line in the case of one vector.

        """
        if coeffs is None:
            raise NameError("Reconstruction needs coefficients")
        self.coeffs = coeffs
        return self._reconstruction(coeff_compute=False, signal_compute=True)


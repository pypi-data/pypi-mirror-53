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
# 0.0.0 First version
# 0.0.2 Bug  correction divide a

import cython
cimport iw.function_fab.stairsum
from iw.function_fab.stairsum cimport stairsum
cimport iw.diaconis_fill.complementschur
from iw.diaconis_fill.complementschur cimport complementschur
cimport iw.diaconis_fill.cal_beta_gamma
from iw.diaconis_fill.cal_beta_gamma cimport cal_beta_gamma
cimport iw.multiresolution.tab_one_step_Lambda
from iw.multiresolution.tab_one_step_Lambda cimport tab_one_step_Lambda
cimport iw.multiresolution.sparsify_matrix
from iw.multiresolution.sparsify_matrix cimport sparsify_matrix
from libc.stdlib cimport  free, malloc
from libc.time cimport time, time_t
cimport numpy as np
import numpy as np
import scipy.sparse as sp
import ctypes


cdef class Graph_c:
    """ A Graph_c class,

    :Example:

    >>> gr = Graph_c(graph_file, opt=None)
    >>> gr._cal_Laplacien()


    - Inputs:

    :param str graph_file: name of graph file
    :param: dict opt: option dictionary
    
    - Attributes::

    :ivar Laplacien: Laplacian of the current graph (original laplacian if no computation has been performed)
    :type Laplacien: 1d array (MemoryView)
    :ivar col: indices of columns of non vanishing entries of Laplacien
    :type col: 1d array (MemoryView)
    :ivar row: indices of rows of non vanishing entries of Laplacien
    :type row: 1d array (MemoryView) 
    :ivar int shape: number of rows of the square matrix Laplacien
    :ivar list entry: instructions for the C programm to sample the roots
    :ivar  int nbr_entry: number of list entries
    :ivar mu_initial: array of value of initial :math:`\\mu`
    :type mu_initial: array
    :ivar dic option_forest: instructions for the C programm to sample the roots
    :ivar dic option_process: instructions and options to run Monte-Carlo simulations for the choice of the optimal q. 
    :ivar int reversible: 1 if the graph is reversible, 0 if not.

    """

    def __cinit__(self, graph_file):
        self._nativePunto = NULL
        self._filloption(graph_file)
        self._graph_init()

    def __init__(self, graph_file):
        self._cal_Laplacien()

    def __getstate__(self):
         return (self.signals,  self.pretreatment, self.nbr_signals, self.graph,
         self.tab_Multires, self.mu_initial, self.reconstructed_s, self.coeffs,
         self.following_size, self.a, self.graph_file_initial,self. process_analysis_flag)

    def __setstate__(self, state):
        (nbr_entry, entry, reversible, origin,
         Laplacien, row, col, shape, option_forest,
         option_process, mu_initial) = state
        self.nbr_entry = nbr_entry
        self.entry = entry
        self.reversible = reversible
        self.origin = origin
        self.Laplacien = Laplacien
        self.row = row
        self.col = col
        self.shape = shape
        self.option_forest = option_forest
        self.option_process = option_process
        self.mu_initial = mu_initial

    cdef _setup_pt(self, num n, param p, punto* pt):
        """ internal function setup internal structures

        - Inputs:

        :param n: num structure contains numerical features
        :type n: num structure
        :param p: param structure contains parameter features
        :type p: param structure
        :param pt: pointer on punto structure contains a table of point features
        :type pt: pointer on punto structure

        - Output:

        :returns: Graph_c itself
        :rtype:  Graph_c

        """
        self._nativeNum = n
        self._nativePunto = pt
        self._nativeParam = p
        self.initialize_reversible()
        return self

    def _nativeNum_function(self):
        """ internal function creates num_dict dictionary from C structure num

        - Output:

        :returns: dict  num_dict  from num internal structure
        :rtype:  dict

        """
        cdef dict num_dict = {}
        num_dict['n'] = < int > self._nativeNum.n
        num_dict['na'] = < int > self._nativeNum.na
        num_dict['ttm'] = self._nativeNum.ttm
        num_dict['tu'] = self._nativeNum.tu
        num_dict['a'] = < int > self._nativeNum.a
        # num_dict['aa'] = self._nativeNum.aa
        num_dict['f'] = < int > self._nativeNum.f
        # num_dict['af'] = self._nativeNum.af
        # num_dict['rg'] = self._nativeNum.rg
        num_dict['q'] = self._nativeNum.q
        num_dict['tmp_inv'] = self._nativeNum.tmp_inv
        num_dict['Z'] = self._nativeNum.Z
        return num_dict

    def _nativeParam_function(self):
        """ internal function creates param_dict dictionary from C structure param

        - Output:

        :returns: dict  param_dict  from param internal structure
        :rtype:  dict

        """
        cdef dict param_dict = {}
        param_dict['da_file'] = self._nativeParam.da_file

        if self._nativeParam.grafo is not NULL and self._nativeParam.da_file:
            str_grafo = self._nativeParam.grafo.decode("UTF-8")
            param_dict['grafo'] = str_grafo
        param_dict['e'] = self._nativeParam.e
        param_dict['fr'] = self._nativeParam.fr
        param_dict['q_min'] = self._nativeParam.q_min
        param_dict['m'] = < int > self._nativeParam.m
        param_dict['z'] = self._nativeParam.z

        param_dict['stampa_foresta'] = self._nativeParam.stampa_foresta
        param_dict['raggiunto'] = self._nativeParam.raggiunto

        param_dict['ancora'] = self._nativeParam.ancora

        param_dict['scrivere'] = self._nativeParam.scrivere
        param_dict['verboso'] = self._nativeParam.verboso
        param_dict['X'] = self._nativeParam.X
        param_dict['immagini'] = self._nativeParam.immagini

        param_dict['contatore'] = self._nativeParam.contatore
        param_dict['scadenza'] = self._nativeParam.scadenza
        param_dict['pausa'] = self._nativeParam.pausa

        param_dict['L'] = self._nativeParam.L
        param_dict['l'] = self._nativeParam.l
        param_dict['soloradici'] = self._nativeParam.soloradici
        param_dict['bordo_si'] = self._nativeParam.bordo_si
        param_dict['ved_att'] = self._nativeParam.ved_att
        param_dict['grandi_radici'] = self._nativeParam.grandi_radici
        param_dict['potenziale'] = self._nativeParam.potenziale
        param_dict['tasso_blu'] = self._nativeParam.tasso_blu
        param_dict['blu_unif'] = self._nativeParam.blu_unif
        if self._nativeParam.foto is not NULL:
            param_dict['foto'] = self._nativeParam.foto
        param_dict['foto_rad'] = self._nativeParam.foto_rad
        param_dict['foto_ext'] = self._nativeParam.foto_ext
        param_dict['nb_foto'] = self._nativeParam.nb_foto
        param_dict['q_foto'] = self._nativeParam.q_foto
        param_dict['fdd'] = self._nativeParam.fdd
        param_dict['num_foto_fatte'] = self._nativeParam.num_foto_fatte
        param_dict['num_istantanee'] = self._nativeParam.num_istantanee
        param_dict['flag_outputfile'] = self._nativeParam.flag_outputfile
        # str_outputfilename = self._nativeParam.outputfilename.decode("UTF-8")
        param_dict['outputfilename'] = self._nativeParam.outputfilename

        param_dict['flag_outputErrorfile'] = self._nativeParam.flag_outputErrorfile
        # str_outputErrorfilename =  self._nativeParam.outputErrorfilename.decode("UTF-8")
        param_dict['outputErrorfilename'] = self._nativeParam.outputErrorfilename

        return param_dict

    def initialize_reversible(self):
        """ set reversible field

        """
        cdef np.ndarray[np.double_t, ndim=1] mu
        cdef int i
        if self._nativePunto[0].pot == -1:
            self.reversible = 0
        else:
            self.reversible = 1
        if self.reversible:
            n = self._nativeNum.n
            mu = np.ndarray(n)
            for i in range(self._nativeNum.n):
                mu[i] = self._nativePunto[i].pot
            self.mu_initial = mu

    def _filloption(self, graph_file=None, option=None):
        """ internal function _fillentry filling of entry option of Graph_c

        - Inputs:

        :param str graph_file: name of graph file
        :param: dict option: optionn dictionary

        """
        if option is None and graph_file is not None:
            option_forest = {'-f': None,
                             '-s': None,
                             '-w': graph_file}
            option_process = {'mod': 'step', 'Nsim': 1}
        elif graph_file is not None:
            option_forest, option_process = self._split_option(option)
            option_forest['-w'] = graph_file
        else:
            option_forest, option_process = self._split_option(option)
            if option_process['mod'] is None:
                option_process = {'mod': 'step'}
            if option_forest['-w'] is None:
                raise ValueError('graph must be initialized')
        self.option_process = option_process
        self.option_forest = option_forest

    @staticmethod
    def _split_option(option):
        """ internal function _split_option split the forest options and process
        option in two different dictionary

        - Input:

        :param double q: q value

        - Output:

        :returns: tuple of dictionaries option_forest, and option_process
        :rtype: tuple of 2 dict

        """
        option_forest = {}
        option_process = {}
        list_key = ['-f', '-q', '-l', '-L', '-s', '-k', '-w']
        for key, value in option.items():
            if key in list_key:
                option_forest[key] = value
            else:
                option_process[key] = value
        return option_forest, option_process

    cpdef _initialise_sample_root(self, double q):
        """internal function initializes c structure and option like it
        should be for sample_root function

        - Input:

        :param double q: q value

        """
        p = self.option_forest['-w']
        self._initialisation_grezza_like()
        self._initialize_basica_end_like()
        self.option_forest['-q'] = q
        self._nativeNum.q = q
        self._nativeParam.da_file = 1
        c_string_s = p.encode("UTF-8")
        self._nativeParam.grafo = c_string_s

    cpdef int _initialise_choixm_q(self, double qmin, double qmax):
        """ internal function initializes c structure and option like it
        should be for choixm_q function

        - Inputs:

        :param double qmin: qmin value
        :param double qmax: qmax value

        - Output:

        :returns: int number of input arguments
        :rtype:  int  number of input arguments

        """
        # print("dans initialise choixq")
        self._initialisation_grezza_like()
        self._initialize_basica_end_like()
        p = self.option_forest['-w']
        # argvS[0] = '-s'
        # self._nativeParam.scrivere = 1
        self._nativeParam.da_file = 1
        c_string_s = p.encode("UTF-8")
        self._nativeParam.grafo = c_string_s
        self.option_forest['-s'] = None
        # self._nativeParam.scrivere = 1
        # argvS[1] = '-f'
        self.option_forest['-f'] = None
        self._nativeParam.fr = 1
        self._nativeParam.m = 0

        self.option_forest['-k'] = qmin
        self._nativeParam.q_min = qmin
        self.option_forest['-q'] = qmax
        self._nativeNum.q = qmax

        # argvS[5] = c_string_qmax
        # argvS[6]= '-w'
        # argvS[7]= graphe_file
        cdef int argcS = 4
        # self._fillentry(p, self.option)
        return argcS

    cpdef _initialisation_grezza_like(self):
        """ internal function initialise c structure and option like grezza

        """
        ###########################################################
        # Initialisation grezza_acquisizione like
        ##############################################################
        cdef  int i
        cdef int ndefL = 1
        cdef int ndefl = 1
        cdef int ndefq = 1

        self._nativeParam.L = 512
        self._nativeParam.l = 512
        self._nativeParam.m = 0
        self._nativeParam.e = 2.0
        self._nativeParam.immagini = 12

        self._nativeParam.pausa = 0
        self._nativeParam.verboso = 1
        self._nativeParam.da_file = 0
        self._nativeParam.z = -1.0
        self._nativeParam.X = 0
        self._nativeParam.stampa_foresta = 0

        self._nativeParam.flag_outputfile = 0
        # value = "./output.txt" #OUTPUTFILE
        # c_string_s = value.encode("UTF-8")
        # self._nativeParam.outputfilename = c_string_s
        self._nativeParam.flag_outputErrorfile = 0
        # value = "./outputerrorfile.txt" #OUTPUTERRORFILE
        # c_string_s = value.encode("UTF-8")
        # self._nativeParam.outputErrorfilename = c_string_s
        self._nativeNum.q = 1.0/512.0

        self._nativeParam.fr = 0
        self._nativeParam.q_min = 0
        self._nativeParam.scrivere = 0

    cpdef _initialize_basica_end_like(self):
        self._nativeParam.scadenza = CLOCKS_PER_SEC * (
                                   (1.0 / self._nativeParam.immagini) -
                                   (self._nativeParam.pausa / 1000.0))
        self._nativeParam.contatore = 0
        self._nativeParam.ancora = 1
        self._nativeParam.raggiunto = 0
        if (self._nativeParam.m):
            self._nativeNum.q = self._nativeNum.ttm
        self._nativeNum.tmp_inv = -1.0
        self._nativeNum.Z = 0.0

    cpdef _cal_Laplacien(self):
        """ function calcul Laplacien from C structure

        """
        cdef long int n = < long int > self._nativeNum.n
        n_int = < int > n
        sps_acc = sp.csc_matrix((n_int, n_int), dtype=np.float64)
        # L = np.zeros((n,n))
        cdef int nv
        for i in range(n_int):
            nv = self._nativePunto[i].nv
            if nv > 0:
                for k in range(nv):
                    neighbors = self._nativePunto[i].vic[k]
                    sps_acc[i, neighbors] += self._nativePunto[i].tass[k]
            sps_acc[i, i] -= self._nativePunto[i].tt

        sps_acc = sps_acc.tocoo()
        self.Laplacien = sps_acc.data
        self.row = sps_acc.row.astype(np.int_)
        self.col = sps_acc.col.astype(np.int_)
        self.shape = sps_acc.shape[0]

    cpdef _cal_C_struct(self):
        """ function calcul C structure from Laplacien

        """
        # print("dans _cal_C_struct")
        if isinstance(self.Laplacien, np.ndarray):
            print("No new internal graph structure can be calculated")
            return

        self._del_struct()
        cdef long int n
        cdef int i
        cdef punto* ptpuntoP
        n = self.shape

        self._nativeNum.n = < long int > n
        self._nativeNum.a = self._nativeNum.n
        self._nativeNum.ttm = 0.0
        self._nativeNum.aa = < long int * > malloc(n * sizeof(long int))
        self._nativeNum.af = < long int * > malloc(n * sizeof(long int))
        self._nativeNum.rg = < long int * > malloc(n * sizeof(long int))
        self._nativeNum.na = 0
        ptpuntoP = < punto * > malloc(n * sizeof(punto))
        if ((not self._nativeNum.aa) or (not self._nativeNum.af) or
           (not self._nativeNum.rg) or (not ptpuntoP)):
            raise MemoryError()
        self._nativePunto = ptpuntoP
        cdef int k, j, nv, k1
        cdef double value
        cdef np.ndarray[np.double_t, ndim=1] temptass
        cdef double* temptassP
        cdef np.ndarray[np.double_t, ndim=1] tempparz_tass
        cdef double* tempparz_tassP
        cdef double temp_sum
        cdef long int* tempvicP
        sps_acc_L = sp.csc_matrix((self.Laplacien, (self.row, self.col)),
                                  shape=(self.shape, self.shape))
        for k in range(n):
            kvalue, k1value, values = sp.find(sps_acc_L[k, :])
            nv = kvalue.size - 1
            if nv < 0:
                nv = 0
            if nv >= 0:
                tempvicP = < long int * > malloc(nv * sizeof(long int))
                if not tempvicP:
                    raise MemoryError()
                self._nativePunto[k].vic = tempvicP
                temptassP = < double * > malloc(nv * sizeof(double))
                if not temptassP:
                    raise MemoryError()
                self._nativePunto[k].tass = temptassP
                tempparz_tassP = < double * > malloc(nv * sizeof(double))
                if not tempparz_tassP:
                    raise MemoryError()
                self._nativePunto[k].somm_parz_tass = tempparz_tassP
                j = 0
                temp_sum = 0
                for k1, value in zip(k1value, values):
                    if k != k1:
                        self._nativePunto[k].vic[j] = < long int > k1
                        self._nativePunto[k].tass[j] = value
                        temp_sum += value
                        self._nativePunto[k].somm_parz_tass[j] = temp_sum
                        j = j + 1
            self._nativeNum.na += nv
            self._nativePunto[k].nv = j
            self._nativePunto[k].tt = temp_sum
            if self._nativePunto[k].tt > self._nativeNum.ttm:
                self._nativeNum.ttm = self._nativePunto[k].tt
        self._initialize_basica_end_like()

    # don’t check for out-of-bounds indexing.
    @cython.boundscheck(False)
    # assume no negative indexing.
    @cython.wraparound(False)
    cpdef  tuple sample_root_q(self, double q, int n):
        """ sample_root_q function

        - Inputs:

        :param double q: q value
        :param int n: number of samples

        - Output:

        :returns: tuple of (R, newR, k) where  Root, 
                new Root and k number of root
        :rtype: tuple of 3 components

        """
        # print("dans sample_root_q")
        cdef int k
        cdef char* graphe_file
        cdef double* Fp
        cdef np.ndarray F
        cdef int size1
        cdef int size2
        cdef int size
        cdef int i
        cdef str qvalue
        cdef np.ndarray R
        cdef np.ndarray r
        cdef np.ndarray rc
        cdef np.ndarray newRc
        cdef num* pt_nn = &self._nativeNum
        cdef param* pt_prm = &self._nativeParam
        cdef punto** pt_pt  =  &self._nativePunto
        self._initialise_sample_root(q)
        rforest_internal(< num* > pt_nn,< punto** > pt_pt, < param* > pt_prm , < double** > &Fp, <int*> &size1, <int*> &size2 )

        size = size1 * size2
        k = size
        F = np.zeros(size)
        for i in range(size):
            F[i] = Fp[i]
        free(Fp)
        F.reshape(size1, size2)
        F = F.reshape(k, 1)
        R = F.astype(dtype=np.int_)
        r = R.reshape(k)
        rc = np.arange(0, n, dtype=np.int_)
        rc = np.where(np.in1d(rc, r, invert=True))[0]
        newRc = rc.reshape(rc.size, 1)
        return (R[:, 0], newRc[:, 0], k)

    # don’t check for out-of-bounds indexing.
    @cython.boundscheck(False)
    # assume no negative indexing.
    @cython.wraparound(False)
    cpdef tuple choixq_m(self, double qmin, double qmax, int Nsim, double a, int n):
        """ choixq_m function

        - Inputs:

        :param double qmin: qmin value
        :param double qmax: qmax value
        :param int Nsim: number of simulations
        :param double a: a value
        :param int n: number of roots

        - Output:

        :returns: tuple of (timebc, taf, itbf, tasurtbf, qc, nRR)
                timebc: vector. Inverse of the discontinuities of the various
                stairs functions, taf: vector. Values of the stair function
                estimating \bar{alpha}, itbf: vector. Values of the stair
                function estimating 1/\beta, itgf:vector. Values of the stair
                function estimating  1/\gamma, tasurtgf: vector. Values of the
                stair function estimating \bar{alpha}/\gamma, tasurtbf: vector.
                Values of the stair function estimating \alpha \bar{alpha}/\beta,
                qc = array of roots corresponding to the first draw, of the current graph
                nRR = corresponding number of elements, of the current graph
        :rtype: tuple 6 arrays
        """
        # print("dans choixq_m")
        cdef double* Fp
        cdef np.ndarray F
        cdef int size1
        cdef int size2
        cdef int i, j
        cdef np.ndarray E
        cdef np.ndarray qc, q
        cdef np.ndarray[np.double_t, ndim=1] nR
        cdef np.ndarray[np.double_t, ndim=1] nRR
        cdef np.ndarray[np.double_t, ndim=1] nRcou
        cdef np.ndarray[np.double_t, ndim=1] nRc
        cdef np.ndarray[np.double_t, ndim=1] tac
        cdef np.ndarray[np.double_t, ndim=1] itbc
        cdef np.ndarray[np.double_t, ndim=1] itgc
        cdef np.ndarray[np.double_t, ndim=1] time
        cdef np.ndarray[np.double_t, ndim=1] timebc, timeac
        cdef np.ndarray[np.double_t, ndim=1] ta
        cdef np.ndarray[np.double_t, ndim=1] taf
        cdef np.ndarray[np.double_t, ndim=1] itgf
        cdef np.ndarray[np.double_t, ndim=1] itbf
        cdef np.ndarray[np.double_t, ndim=1] tasurtgf
        cdef np.ndarray[np.double_t, ndim=1] tasurtbf
        # call _initialise_choixm_q to set correctly pointer,
        # option and variables
        cdef int argcS = self._initialise_choixm_q(qmin, qmax)
        cdef num* pt_nn = &self._nativeNum
        cdef param* pt_prm = &self._nativeParam
        cdef punto** pt_pt  =  &self._nativePunto

        #################################################################################
        # external function rforest_internal, works with pointers num* , param*, punto**
        #################################################################################
        rforest_internal(<num*> pt_nn,<punto**> pt_pt, <param*> pt_prm , <double**> &Fp, <int*> &size1, <int*> &size2 )
        # recuperation of output variable Fp, size1, size2
        F = np.zeros(size1*size2)
        for i in range(size1*size2):
            F[i] = Fp[i]
        free(Fp)
        E = F.reshape(size1, size2).transpose()
        qc = E[0, :]
        nR = E[1, :]
        nRR = nR
        # nRcou = nR.copy()
        nRc = n - nR
        # Bug 0.0.2 correction / nRc +1
        tac = np.divide(nRc, nR+1)
        itbc = np.divide(nRc, nR)
        # Bug 0.0.2 correction divide /a
        # itbc = itbc / a
        # itgc = n / (1+nRc)
        timebc = 1.0 / qc
        for j in range(1, Nsim):
            self._initialise_choixm_q(qmin,  qmax)
            pt_nn = &self._nativeNum
            pt_prm = &self._nativeParam
            pt_pt = &self._nativePunto

            rforest_internal(<num*> pt_nn, <punto**> pt_pt, <param*> pt_prm, <double**> &Fp, <int*> &size1, <int*> &size2 )       
            F = np.zeros(size1*size2)
            for i in range(size1*size2):
                F[i] = Fp[i]
            free(Fp)

            E = F.reshape(size1, size2).transpose()
            q = E[0, :]
            nR = E[1, :]
            nRc = n - nR
            time = 1.0 / q
            # Calcul des estimées de la moyenne et de la variance du nombre de racines.
            # timeRc, nRcou = stairsum(<np.ndarray> time, <np.ndarray> nR,
            #                        <np.ndarray>  timec,<np.ndarray> nRcou)

            # Calcul des estimées de la moyenne et de la variance
            # du nombre de racines.
            # Calcul des estimées de alphabar, beta, gamma.
            ta = np.divide(nRc, (nR+1))
            timeac, tac = stairsum(<np.ndarray> time, <np.ndarray> ta,
                                   <np.ndarray> timebc, <np.ndarray> tac)
            itb = np.divide(nRc, nR)
            timebc, itbc = stairsum(<np.ndarray> time, <np.ndarray>  itb,
                                    <np.ndarray> timebc,<np.ndarray>  itbc)
            # itg = np.divide(n, (1+nRc))
            # timec, itgc = stairsum(<np.ndarray> time, <np.ndarray>  itg,
            #                       <np.ndarray> timec,<np.ndarray> itgc)

        # nRcou = nRcou / Nsim
        taf = tac / Nsim
        #print(timec.asarray().shape)
        #print(taf.shape)
        # itgf = itgc / Nsim

        # tasurtgf = taf * itgf
        taf = np.divide(taf, timebc)
        # itgf = itgf * timec

        itbf = itbc / Nsim
        tasurtbf = taf * itbf
        itbf = itbf / a
        # return timec, nRcou, taf, itbf, itgf, tasurtgf, tasurtbf
        return timebc, taf, itbf, tasurtbf, qc, nRR

    # don’t check for out-of-bounds indexing.
    @cython.boundscheck(False)
    # assume no negative indexing.
    @cython.wraparound(False)
    cpdef  tuple tab_one_step_Lbarre_sparse(self, double[:] L,
                                            long int[:] row, long int[:] col,
                                            int shape,
                                            double a, double[:] mu,
                                            int step, int n, double theta):
        """tab_one_step_Lbarre_sparse function


        - Inputs:

        :param L: a Laplacian matrix 1d sparse matrix
        :type L: numpy 1d double array
        :param row: row array of sparse matrix L
        :type row: numpy 1d int array
        :param col: column array of sparse matrix L
        :type col: numpy 1d int array
        :param int shape: shape of L matrix
        :param graph: graph to populate
        :type graph: Graph_c class
        :param double a: max(abs(L(x,x))
        :param mu: measure of reversibility. In the case the laplacian is
                 symetric it has to be the uniform measure.
        :type mu: numpy 1d double array
        :param int step: iteration index in the case of multiresolution
        :param int n: -cardinal of the entire set

        - Outputs:

        :param Lbarres:  Lbarres matrix 1d sparse  matrix sparcified Schur
               complement of [L]_Rc in L
        :type Lbarres: 1d double array
        :param row_brs: row array of sparse matrix Lbarres
        :type row_brs: 1d int_ array
        :param col_brs: column array of sparse matrix Lbarres
        :type col_brs: 1d int_ array
        :param int shape_brs: shape of Lbarres matrix
        :param Lbarre:  Lbarre matrix 1d sparse matrix
               Lbarre is Schur complement of [L]_Rc in L
        :type Lbarre: 1d double array
        :param row1: row array of sparse matrix Lbarre
        :type row1: 1d int_ array
        :param col1: column array of sparse matrix Lbarre
        :type col1: 1d int_ array
        :param int shape1: shape of Lbarre matrix
        :param GXbarrebr: GXbarrebr matrix 1d sparse  matrix
                        GXbarrebr: it is the matrix (-L_(Xbreve,Xbreve))^{-1}
        :param row2: row array of sparse matrix GXbarrebr
        :type row2: 1d int_ array
        :param col2: column array of sparse matrix GXbarrebr
        :type col2: 1d int_ array
        :param int shape2: shape of GXbarrebr matrix
        :param Lambdabarre: Lambdabarre matrix 1d sparse  matrix
        :type Lambdabarre: 1d double array
        :param row_lambdabr: row array of sparse matrix Lambdabarre
        :type row_lambdabr: 1d int_ array
        :param col_lambdabr: column array of sparse matrix Lambdabarre
        :type col_lambdabr: 1d int_ array
        :param int shape0_lamdabr: shape dimension 0 of Lambdabarre matrix
        :param int shape1_lamdabr: shape dimension 1 of Lambdabarre matrix
        :param Lambdabreve: Lambdabreve matrix 1d sparse  matrix
        :type Lambdabreve: 1d double array
        :param row_lambdabv: row array of sparse matrix Lambdabreve
        :type row_lambdabv: 1d int_ array
        :param col_lambdabv: column array of sparse matrix Lambdabreve
        :type col_lambdabv: 1d int_ array
        :param int shape0_lamdabv: shape dimension 0 of Lambdabreve matrix
        :param int shape1_lamdabv: shape dimension 1 of Lambdabreve matrix
        :param graph: graph populated
        :type graph: Graph_c class

        """
        # print("dans tab_one_step_Lbarre_sparse")
        cdef double qmin
        cdef double qmax
        cdef int Nsim
        cdef int i, x
        cdef np.ndarray[np.double_t, ndim=1] timec, nRcou, taf
        cdef np.ndarray[np.double_t, ndim=1] nRR
        cdef np.ndarray qc
        cdef np.ndarray[np.double_t, ndim=1] itbf, itgf, tasurtgf, tasurtbf
        cdef double valmin
        cdef int indtimeopt
        cdef np.ndarray[np.int_t, ndim=1] Xbarre
        cdef np.ndarray[np.int_t, ndim=1] Xbreve
        cdef double q
        cdef int k
        cdef double timeopt
        cdef np.ndarray[np.double_t, ndim=1] Lbarre, GXbarrebr
        cdef np.ndarray[np.int_t, ndim=1] row1, col1, row2, col2
        cdef np.ndarray[np.double_t, ndim=1] seuil 
        cdef int shape1, shape2
        cdef double alphabar
        if step != 0:
            self.Laplacien = L
            self.row = row
            self.col = col
            self.shape = shape
            self._cal_C_struct()
            self.option_forest['-w'] = self.option_forest['-w'] + '_' + str(step)

        qmin = a / 8.
        qmax = a
        Nsim = self.option_process['Nsim']
        # (timec, nRcou, taf,
        # itbf, itgf, tasurtgf, tasurtbf)
        (timec, taf, itbf, tasurtbf, qc, nRR) = self.choixq_m(qmin, qmax,
                                                     Nsim, a, n)
        indtimeopt = tasurtbf.argmin()
        valmin = tasurtbf.min()
        timeopt = < double > timec[indtimeopt]
        q = 1.0 / (timeopt)
        (Xbarre, Xbreve, k) = self.sample_root_q(q, n)
        # compteur = 0
        while (Xbreve.size == 0):
            (Xbarre, Xbreve, k) = self.sample_root_q(q, n)
            # compteur += 1
        cardXbar = Xbarre.size
        # % Calcul de Lambdabarre
        (Lbarre, row1, col1, shape1, alphabar,
         GXbarrebr, row2, col2, shape2) = complementschur(L, row, col, shape,
                                                          Xbarre, Xbreve)
        # %calcul de gamma et beta
        gam, beta = cal_beta_gamma(L, row,  col, shape,
                                   GXbarrebr, row2, col2, shape2,
                                   Xbarre, Xbreve, a)
        mubarre = np.zeros(Xbarre.size, dtype=np.double)
        # mubarre = mu[Xbarre] does not work
        i = 0
        for x in Xbarre:
            mubarre[i] = mu[x]

        if mubarre.size > 0:
            mubarre = mubarre / (np.sum(mubarre))
        (Lambdabarre, row_lambdabr, col_lambdabr, shape0_lamdabr, shape1_lamdabr,
         Lambdabreve, row_lambdabv, col_lambdabv, shape0_lamdabv, shape1_lamdabv,
         qprime) = tab_one_step_Lambda(a, L, row, col, shape, Xbarre, Xbreve, n)

        sLambdabarre = sp.csr_matrix((Lambdabarre,
                                      (row_lambdabr, col_lambdabr)),
                                     shape=(shape0_lamdabr, shape1_lamdabr))
        sLbarre = sp.csr_matrix((Lbarre, (row1, col1)), shape=(shape1, shape1))
        sL = sp.csr_matrix((L, (row, col)), shape=(shape, shape))

        temp = sLambdabarre.dot(sL) - sLbarre.dot(sLambdabarre)
        DF = abs(temp)

        if DF.shape[0] > 0:
            threshold = (DF.sum(axis=1) / (2*theta*a)) * alphabar
        else:
            raise ValueError("Vector size is null")
        seuil = np.zeros(threshold.shape[0], dtype=np.double)
        for i in range(threshold.shape[0]):
            seuil[i] = threshold[i, 0]
        (Lbarres, row_brs, col_brs,
         shape_brs) = sparsify_matrix(Lbarre,
                                      row1, col1,
                                      shape1, seuil)
        return (Lbarres, row_brs, col_brs, shape_brs,
                Lbarre, row1, col1, shape1,
                mubarre, Xbarre, Xbreve,
                alphabar, gam, beta,
                GXbarrebr, row2, col2, shape2, q, qprime,
                Lambdabarre, row_lambdabr, col_lambdabr,
                shape0_lamdabr, shape1_lamdabr,
                Lambdabreve, row_lambdabv, col_lambdabv,
                shape0_lamdabv, shape1_lamdabv
                )

    def __dealloc__(self):
        self._del_struct()

    def _del_struct(self):
        free(self._nativeNum.aa)
        free(self._nativeNum.af)
        free(self._nativeNum.rg)
        n = < int > self._nativeNum.n
        for i in range(n):
            free(self._nativePunto[i].vic)
            free(self._nativePunto[i].somm_parz_tass)
            free(self._nativePunto[i].tass)
        free(self._nativePunto)

    def _graph_init(self):
        cdef int r_grezza, re_iniz, re_cal
        cdef int i
        cdef num nn
        cdef param prm
        cdef punto* pt
        cdef int nbr_entry
        cdef char* c_string

        s = set(self.option_forest.values())
        s.remove(None)
        nbr_entry = len(self.option_forest) + len(s)
        cdef char** entry = < char ** >malloc(nbr_entry * sizeof(char*))
        if not entry:
            raise MemoryError()
        self.entry = []  # dtype=np.dtype((bytes, 1))
        self.nbr_entry = nbr_entry
        i = 0
        for key, value in self.option_forest.items():
            key = key.encode('UTF-8')
            self.entry.append(key)
            c_string = key
            entry[i] = c_string
            if value is not None:
                i = i + 1
                if type(value) is not str:
                    value = str(value)
                value = value.encode('UTF-8')
                self.entry.append(value)
                c_string = value
                entry[i] = c_string
            i = i + 1
#         entry[0] = b'-s'
#         entry[1] = b'-f'
#         entry[3] = b'-w'
#         value = self.option_forest['-w'].encode('UTF-8')

#
#         c_string = value
#         entry[4] = c_string
        r_grezza = grezza_acquisizione(nbr_entry, <char**> entry, <num*> &nn, <param*> &prm)

        re_iniz = inizializzazione_basica(<num* > &nn, <punto**> &pt, <param*> &prm)

        re_cal = calcolare_potenziale(< num* > &nn, < punto** > &pt)
        if r_grezza != 0 or re_iniz != 0 or re_cal != 0:
            raise MemoryError()

        free(entry)

        return self._setup_pt(nn, prm, pt)

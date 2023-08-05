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
# file grapgh_c.pxd
from libc.stdio cimport FILE
from cpython cimport bool

cdef extern from "<time.h>" nogil:
    ctypedef long clock_t
    ctypedef long time_t
 
    enum: CLOCKS_PER_SEC
    clock_t clock()             # CPU time
    time_t time(time_t *) # wall clock time since Unix epoch

cdef extern from "kernel_c/cuore.h": # from "cuore.h"

    ctypedef struct punto:
        int nv
        long int* vic
        double* tass
        double* somm_parz_tass
        double tt
        double pot
        double massa
        long int succ
        long int rad
        int attivo
        long int prima
        long int dopo
        int x
        int y
        int intens
        int wilson
        pass

    ctypedef struct num:
        long int n # points' number of graph
        long int na # ribs' number of graph
        double ttm
        double tu
        long int a
        long int* aa
        long int f
        long int* af
        long int* rg
        double q
        double tmp_inv
        double Z
        pass

    int tutti_svegli_tempo_zero(num* nn_p, punto** pt_p)

cdef extern from "kernel_c/lodge.h":  # from "lodge.h"
    cdef char*  OUTPUTFILE = "./output.txt"
    cdef char*  OUTPUTERRORFILE  = "./outputerrorfile.txt"

    ctypedef struct param:
        int da_file
        char* grafo
        long int m
        double e
        int fr
        double q_min
        double z
        int stampa_foresta
        int raggiunto
        int ancora
        int scrivere
        int verboso
        int X
        int immagini
        int contatore
        double scadenza
        int pausa
        void* img_p
        char* nome
        int L
        int l
        int soloradici
        int bordo_si
        int ved_att
        int caric_manc
        int grandi_radici
        int potenziale
        int tasso_blu
        int blu_unif
        char* foto
        char foto_rad[100]
        char foto_ext[100]
        int nb_foto
        double q_foto
        double fdd
        int num_foto_fatte
        int num_istantanee
        int flag_outputfile
        char* outputfilename
        FILE* outputfile
        int flag_outputErrorfile
        char* outputErrorfilename
        FILE* outputErrorfile
        pass

    int inizializzazione_basica(num* nn_p, punto** pt_p, param* prm_p)
    int grezza_acquisizione(int argc, char* argv[], num* nn_p, param* prm_p)
    int calcolare_potenziale(num* nn_p, punto** pt_p)


cdef extern from "kernel_c/rforest_internal.h": # from "rforest_internal.h":
    int rforest_internal(num* nn_p, punto** pt_p,param* prm_p, double** pt_out, int* pt_size1, int* pt_size2)


cdef class Graph_c:
    cdef public int nbr_entry
    cdef public list entry
    cdef public int reversible
    cdef public double[:] Laplacien
    cdef public long int[:] row
    cdef public long int[:] col
    cdef public int shape
    cdef public dict option_forest
    cdef public dict option_process
    cdef public double[:] mu_initial

    cdef num _nativeNum
    cdef punto* _nativePunto
    cdef param _nativeParam
    cdef _setup_pt(self, num n, param p, punto* pt)

#    cpdef dict _nativeNum_function(self)
#    cpdef dict _nativeParam_function(self)
#    cpdef _fillentry(self, graph_file, option)
    cpdef _cal_Laplacien(self)
    cpdef _cal_C_struct(self)
    cpdef _initialise_sample_root(self, double q)
    cpdef int _initialise_choixm_q(self, double qmin, double qmax)
    cpdef _initialisation_grezza_like(self)
    cpdef tuple sample_root_q(self, double q, int n)
    cpdef tuple choixq_m(self, double qmin, double qmax, int Nsim, double a, int n)
    cpdef tuple tab_one_step_Lbarre_sparse(self, double[:] L, long int[:] row, long int[:] col, int shape, double a, double[:] mu, int step, int n, double theta)
    cpdef _initialize_basica_end_like(self)
#cdef int acquisition(int argc, char* argv[], num* nn_p, param* prm_p)
#cdef int cal_potential(num* nn_p, punto** pt_p)
#cdef int initialise(num* nn_p, punto** pt_p, param* prm_p)
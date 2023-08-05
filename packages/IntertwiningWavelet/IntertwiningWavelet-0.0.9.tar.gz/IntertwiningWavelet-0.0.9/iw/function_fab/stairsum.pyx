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
cimport numpy as np


# don’t check for out-of-bounds indexing.
@cython.boundscheck(False)
# assume no negative indexing.
@cython.wraparound(False)
cpdef tuple stairsum(double[:] q,
                     double[:] R,
                     double[:] qq,
                     double[:] RR):
    """stairsum function 
    This function computes the sum of two stairs functions. The stairs
    functions are assumed to be right continuous, with discontinuities
    at points q, qq, and respective
    values at this points given respectively by R and RR

    - Inputs:

    :param q: vector of the discontinuities points of the first function
    :type q:  1d double array
    :param R: vector of the same length as q, containing the values of the
           first function at points given by q
    :type R: 1d double array
    :param qq: vector of the discontinuities points of the second function
    :type qq: 1d double array
    :param RR: vector of the same length as qq, containing the values of the second function at
           points given by qq
    :type RR: 1d double array

    - Output:

    :returns: tuple of (qs, Rs) where qs vector of the discontinuities points
            of the sum of the two functions. Due to the continuity, some of
            the values of q or qq are ignored and Rs vector of the same
            length as qs, containing the values of the  sum of the two
    :rtype: tuple of 2 arrays

    """

    # Sorting of q and R by inscreasing order of q
    cdef np.ndarray[np.int_t, ndim=1] I, II, Is, Isq, Isqq
    cdef np.ndarray[np.int_t, ndim=1] Isqinter, Isqqinter
    #cdef np.ndarray[np.double_t, ndim=1] Rprime, RRprime
    cdef np.ndarray[np.double_t, ndim=1] Rs
    cdef np.ndarray[np.double_t, ndim=1] qs
    cdef int nqq, nq
    # Erasing multiple values and sorting by increasing order.
    (q, I) = np.unique(q, return_index=True)
    Rprime = np.asarray(R)
    Rprime = Rprime[I]
    nq = q.size

    # Sorting of qq and RR by inscreasing order of qq
    qq, II = np.unique(qq, return_index=True)
    RRprime = np.asarray(RR)
    RRprime = RRprime[II]
    nqq = qq.size

    # Defining the discontinuities of the sum
    qs = np.concatenate((q, qq))
    Is = np.argsort(qs)
    qs = qs[Is]
    Is = Is + 1
    Isq = np.cumsum(Is <= nq)
    Isqq = np.cumsum(Is > nq)

    # Erasing the values of qs for which one of the function is not defined.
    Isqinter = (Isq > 0).astype(int)
    Isqqinter = (Isqq > 0).astype(int)
    I = np.logical_and(Isqinter, Isqqinter).astype(int)

    qs = qs[np.where(I)]
    Isq = Isq[np.where(I)]
    Isqq = Isqq[np.where(I)]

    # Defining the values of the sum at points given by qs;
    Rs = Rprime[Isq - 1] + RRprime[Isqq - 1]
    # Erasing values which are the same in q and qq.
    qs, Is = np.unique(qs, return_index=True)
    # Rs = Rs[Is] - 1
    Rs = Rs[Is-1]
    return qs, Rs

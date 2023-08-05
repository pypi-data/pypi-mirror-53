#!/usr/bin/env python3
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
"""
Created on Fri Jul 19 14:43:10 2019

@author: melot &stordeur
"""
import numpy as np
import scipy.io as si

def write_gsp_to_g(W,name):
    """
    This function writes the file encoding the weight matrix of a graph that can be used by 
    iw
    
    - Inputs::
    
    :param W:    Weight matrix of a graph
    :type W:    Sparse Scipy matrix
    :param name: Name of the file to fill in, better to identify with a .g termination
    :type name:  String 
    
    - Output::
        
    :return: writes the file .g in iw style
    :rtype: file
    """   
       
    f = open(name, 'w+')
    f.write('numero_di_vertici %d\n'%(W.shape[0]))
    x=0

#Preprocess the sparse matrix
    N=W.shape[0]
    zerodia=np.zeros((N,))
    W.setdiag(zerodia,0)
    W = np.abs(W)

# Download the indices of non zeros entries.
    liste = np.nonzero(W)
    liste = np.transpose(liste)

# Give the list of non zeros entries per row
    A = np.diff(W.tocsr().indptr) 
    
    y = []
    for i in range(A.size) :

        y.append(liste[x:x+A[i],1])
        x = x + A[i]
        f.write('vertice %8d numero_di_vicini %8d\n' %(i, A[i]))

        for j in range(len(y[i])):
            
            f.write('vicino %8d  tasso %e \n' %(y[i][j], W[i,y[i][j]]))

    return  y

    f.close()
    
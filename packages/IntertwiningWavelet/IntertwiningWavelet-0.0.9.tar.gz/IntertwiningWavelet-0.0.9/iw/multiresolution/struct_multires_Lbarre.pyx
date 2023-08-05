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
import numpy as np
cimport cython
cimport numpy as np
cimport iw.reconstruction.operateur_reconstruction_one_step
from iw.reconstruction.operateur_reconstruction_one_step cimport operateur_reconstruction_one_step
cimport iw.graph_c
from iw.graph_c cimport Graph_c


cdef class Tab_Struct_multires_Lbarre:
    """This Class computes the new subgraph, the matrix of the Laplacian
    of the new subgraph, the matrix Lambda
    (which is built through Lambdabreve and Lambdabarre
    from the approximate solution 1 of Diaconis-Fill equation.
    This means:

    - Lbarre is the Schur complement of L_Rc in L with Rc
      the complement of the set Xbarre

    - Lambda is the matrix whose rows vectors are
      :math:`\\nu_{xbarre} = P_{xbarre} (X(T_{q'}))` and
      :math:`\\Psi_{xbreve} = (-Id + K_{q'})[xbreve, :]`
      and keeps them in two elements :py:data:`Struct_Mana_re` (array of
      :py:class:`Struct_M_ana_recons` class) and
      :py:data:`Struct_Mres_gr` (array of
      :py:class:`Struct_multires_Lbarre` class).

    - Inputs:

    :param graph: graph is the current graph for this step of calculation
    :type graph: :py:class:`iw.graph_c.Graph_c` class.
    :param mu: measure of reversibility. In the case the
           laplacian is symetric it has to be the uniform measure.
    :type mu: 1d double array
    :param int n: size of the set of vertices
    :param mod: define the mod of multiscale calculations:

                    * 'step' determine the number of steps for decomposition

                    * 'card' determine the minimum cardinal of graph
    :type mod: string
    :param int m: number of maximum nodes to stop the decomposition
           lowerbound on the size of Xbarre
    :param int steps: number of steps to stop the decomposition
    :param double theta: parameter for sparsification threshold

    - Attributes::

    :ivar Struct_Mres_gr: array of :class:`iw.multiresolution.struct_multires_Lbarre.Struct_multires_Lbarre`
    :type Struct_Mres_gr: 1d object array
    :ivar Struct_Mana_re: array of :class:`iw.multiresolution.struct_multires_Lbarre.Struct_M_ana_recons`
    :type Struct_Mana_re: 1d object array
    :ivar int steps: number of level of decomposition
    """

    def __cinit__(self, Graph_c graph, double a, double[:] mu,
                  int n, str mod, int  m, int steps, double theta):
        pass

    def __getstate__(self):
         return  (self.Struct_Mres_gr, self.Struct_Mana_re, self.steps)

    def __setstate__(self, state):
        (Struct_Mres_gr, Struct_Mana_re, steps) = state
        self.Struct_Mres_gr = Struct_Mres_gr
        self.Struct_Mana_re = Struct_Mana_re
        self.steps = steps


    def __init__(self, Graph_c graph, double a, double[:] mu,
                 int n, str mod, int m, int steps, double theta):
        # print("dans Tab_Struct_multires_Lbarre")
        # mod = 'step'
        cdef int n0 = n
        ############################################################
        # Definition of mod default associated values
        ############################################################
        if 'step' in mod:
            if steps is None:
                steps = n0 // 4
            #: number of steps
            self.steps = steps
            # """ number of steps """
        elif 'card' in mod and m is None:
            m = 10
            self.steps = 0

        cdef double alphabar0 = < double > a
        cdef double[:] mu0 = mu.copy()
        cdef int i = 0
        cdef int b0 = n
        epsilon = np.finfo(float).eps
        if 'card' in mod:
            while (n0 > m) and alphabar0 > epsilon:
                n0, shapeb0, graph, alphabar0 = self._decomposition(i, graph,
                                                                    alphabar0,
                                                                    mu0, n0, theta)
                b0 = shapeb0
                i = i + 1
            self.steps = i

        elif mod.startswith('step'):
            self.steps = steps
            for i in range(steps):
                if n0 >= 2 and alphabar0 > epsilon:
                    n0, b0, graph, alphabar0 = self._decomposition(i, graph,
                                                                   alphabar0,
                                                                   mu0, n0, theta)
                else:
                    self.steps = i
                    break

    cpdef tuple _decomposition(self, int i, Graph_c graph,
                               double alphabar0, double[:] mu0,
                               int n0, double theta):
        """Internal function _decomposition which performs the calculations for one
        step

        - Inputs:

        :param int i: iteration index in the case of multiresolution.
        :param graph: graph is the current graph for this step of calculation
        :type graph: :py:class:`iw.graph_c.Graph_c` object of iw package
        :param double alphabar0: new maximum of the aboslute value
               of the diagonal indices of Lbarre
        :param mu0: measure of reversibility. In the case the
               laplacian is symetric it has to be the uniform measure.
        :type mu0: 1d double array
        :param int n0: size of the set of vertices
        :param double theta: parameter for sparsification threshold

        """
        #  Declaration
        cdef double[:] L
        cdef long int[:] row
        cdef long int[:] col
        cdef int shape

        cdef np.ndarray[np.double_t, ndim=1] Lbarre0
        cdef np.ndarray[np.int_t, ndim=1] rowba0
        cdef np.ndarray[np.int_t, ndim=1] colba0
        cdef int shapeba0

        cdef double[:] Lbarres0
        cdef long int[:] rowbas0
        cdef long int[:] colbas0
        cdef int shapebas0

        cdef double[:] GXbarrebr0
        cdef long int[:] rowGX0
        cdef long int[:] colGX0
        cdef int shape_GX0

        cdef long int[:] Xbarre0, Xbreve0
        cdef double[:] Lamdabarre0, Lambdabreve0
        cdef long int[:] row_lambdabarre0, col_lambdabarre0
        cdef long int[:] row_lambdabreve0, col_lambdabreve0
        cdef int shape0_lambdabarre0, shape1_lambdabarre0
        cdef int shape0_lambdabreve0, shape1_lambdabreve0

        cdef double gam0, beta0, q0, qprime0

        if i == 0:
            L = graph.Laplacien
            row = graph.row
            col = graph.col
            shape = graph.shape
        if i > 0:
            L = self.Struct_Mres_gr[i-1].Lbarres
            row = self.Struct_Mres_gr[i-1].rowLbarres
            col = self.Struct_Mres_gr[i-1].colLbarres
            shape = self.Struct_Mres_gr[i-1].shapeLbarres
        #######################################################################
        # function tab_one_step_Lbarre_sparse of graph
        #######################################################################
        (Lbarres0, rowbas0, colbas0, shapebas0,
         Lbarre0, rowba0, colba0, shapeba0,
         mu0, Xbarre0, Xbreve0,
         alphabar0, gam0, beta0,
         GXbarrebr0, rowGX0, colGX0, shape_GX0, q0, qprime0,
         Lamdabarre0, row_lambdabarre0, col_lambdabarre0,
         shape0_lambdabarre0, shape1_lambdabarre0,
         Lambdabreve0, row_lambdabreve0, col_lambdabreve0,
         shape0_lambdabreve0, shape1_lambdabreve0
         ) = graph.tab_one_step_Lbarre_sparse(L, row, col, shape,
                                              alphabar0, mu0, i, n0, theta)
        #######################################################################
        # Filling the structure Struct_Mres_gr analysis
        #######################################################################
        if i == 0:
            self.Struct_Mres_gr = np.array([Struct_multires_Lbarre(
                                            Lbarre0, rowba0, colba0, shapeba0,
                                            Lbarres0, rowbas0, colbas0, shapebas0,
                                            alphabar0, mu0,
                                            Xbarre0,
                                            gam0, beta0, q0, qprime0)])
        else:
            self.Struct_Mres_gr = np.append(self.Struct_Mres_gr, Struct_multires_Lbarre(
                                            Lbarre0, rowba0, colba0, shapeba0,
                                            Lbarres0, rowbas0, colbas0, shapebas0,
                                            alphabar0, mu0,
                                            Xbarre0,
                                            gam0, beta0, q0, qprime0))

        #######################################################################
        # function operateur_reconstruction_one_step
        #######################################################################
        (Rbarre, rowlra, collra, shape0_lra, shape1_lra,
         Rbreve, rowlrb, collrb, shape0_lrb, shape1_lrb
         ) = operateur_reconstruction_one_step(
            L, row, col, shape,
            Lbarre0, rowba0, colba0, shapeba0,
            GXbarrebr0, rowGX0, colGX0, shape_GX0,
            Xbarre0, qprime0)
        #######################################################################
        # Filling the structure Struct_M_ana_recons analysis
        # and reconstruction operator
        #######################################################################
        if i == 0:
            self.Struct_Mana_re = np.array([Struct_M_ana_recons(
                Lamdabarre0, row_lambdabarre0, col_lambdabarre0,
                shape0_lambdabarre0, shape1_lambdabarre0,
                Lambdabreve0, row_lambdabreve0, col_lambdabreve0,
                shape0_lambdabreve0, shape1_lambdabreve0,
                Rbarre, rowlra, collra, shape0_lra, shape1_lra,
                Rbreve, rowlrb, collrb, shape0_lrb, shape1_lrb)])
        else:
            self.Struct_Mana_re = np.append(
                self.Struct_Mana_re, Struct_M_ana_recons(
                    Lamdabarre0, row_lambdabarre0, col_lambdabarre0,
                    shape0_lambdabarre0, shape1_lambdabarre0,
                    Lambdabreve0, row_lambdabreve0, col_lambdabreve0,
                    shape0_lambdabreve0, shape1_lambdabreve0,
                    Rbarre, rowlra, collra, shape0_lra, shape1_lra,
                    Rbreve, rowlrb, collrb, shape0_lrb, shape1_lrb))
        return Xbarre0.size, Xbreve0.size, graph, alphabar0


cdef class Struct_multires_Lbarre:
    """ Class Struct_multires_Lbarre
    this class saves Inputs of analysis computation in its attribute

    - Inputs:

    :param Lbarre:  Lbarre matrix 1d sparse matrix
           Lbarre is Schur complement of [L]_Rc in L 
           :py:func:`iw.diaconis_fill.complementschur`
           with Rc the complement of the set Xbarre
    :type Lbarre: 1d double array
    :param row1b: row array of sparse matrix Lbarre
    :type row1b:  1d int_ array
    :param col1b: column array of sparse matrix Lbarre
    :type col1b:  1d int_ array
    :param int shapelb: shape of Lbarre matrix
    :param Lbarres:  Lbarres matrix 1d sparse  matrix
                  sparcified Schur complement of [L]_Rc in L
    :type Lbarres: 1d double array
    :param rowlbs: row array of sparse matrix Lbarres
    :type rowlbs: 1d int_ array
    :param collbs: column array of sparse matrix Lbarres
    :type collbs: 1d int_ array
    :param int shapelbs: shape of Lbarres matrix
    :param double alphabar: max(abs(L(x,x))
    :param mu: measure of reversibility. In the case the
             laplacian is symetric it has to be the uniform measure.
    :type mu:  1d double array
    :param Xbarre: vector of nR indices corresponding to the part of matrix L
    :type Xbarre:  1d int_ array
    :param double gamma: value of gamma : numeric.
                       1/gamma= maximum Hitting time
    :param double beta: value of beta : mean time of return
                      after the first step
    :param double q: parameter to sample the vertices of the new graph
    :param double qprime: parameter to compute the solution of
                        Diaconis-Fill equation

    - Attributes::

    :ivar Lbarre:  Lbarre matrix 1d sparse matrix
           Lbarre is Schur complement of [L]_Rc in L
           :py:func:`iw.diaconis_fill.complementschur`
           with Rc the complement of the set Xbarre
    :type Lbarre: 1d double array
    :ivar rowLbarre: row array of sparse matrix Lbarre
    :type rowLbarre:  1d int_ array
    :ivar colLbarre: column array of sparse matrix Lbarre
    :type colLbarre:  1d int_ array
    :ivar int shapeLbarre: shape of Lbarre matrix
    :ivar Lbarres:  Lbarres matrix 1d sparse  matrix
                  sparcified Schur complement of [L]_Rc in L
    :type Lbarres: 1d double array
    :ivar rowLbarres: row array of sparse matrix Lbarres
    :type rowLbarres: 1d int_ array
    :ivar colLbarres: column array of sparse matrix Lbarres
    :type colLbarres: 1d int_ array
    :ivar int shapeLbarres: shape of Lbarres matrix
    :ivar double alphabar: max(abs(L(x,x))
    :ivar mubarre: measure of reversibility. In the case the
             laplacian is symetric it has to be the uniform measure.
    :type mubarre:  1d double array
    :ivar Xbarre: vector of nR indices corresponding to the part of matrix L
    :type Xbarreu:  1d int_ array
    :ivar double gamma: value of gamma : numeric.
                       1/gamma= maximum Hitting time
    :ivar double beta: value of beta : mean time of return
                      after the first step
    :ivar double q: parameter to sample the vertices of the new graph
    :ivar double qprime: parameter to compute the solution of
                        Diaconis-Fill equation

    """

    def __cinit__(self, double[:] Lbarre, long int[:] rowlb, long int[:] collb, int shapelb,
                  double[:] Lbarres, long int[:] rowlbs, long int[:] collbs, int shapelbs,
                  double alphabar, double[:] mu, long int[:] Xbarre,
                  double gamma, double beta, double q, double qprime):
        pass

    def __init__(self, double[:] Lbarre, long int[:]  rowlb, long int[:] collb, int shapelb,
                 double[:] Lbarres, long  int[:] rowlbs, long  int[:] collbs ,int shapelbs,
                 double alphabar, double[:] mu,  long int[:] Xbarre,
                 double gamma, double beta, double q, double qprime):

        self.Lbarre = Lbarre
        self.rowLbarre = rowlb
        self.colLbarre = collb
        self.shapeLbarre = shapelb

        self.Lbarres = Lbarres
        self.rowLbarres = rowlbs
        self.colLbarres = collbs
        self.shapeLbarres = shapelbs

        self.mubarre = mu
        self.Xbarre = Xbarre

        self.alphabar = alphabar
        self.gamma = gamma
        self.beta = beta

        self.q = q
        self.qprime = qprime

    def __getstate__(self):
         return  (self.Struct_Mres_gr, self.Struct_Mana_re, self.steps)

    def __setstate__(self, d):
         self.Lbarre  = d['Lbarre']
         self.rowLbarre = d['rowLbarre']
         self.colLbarre = d['colLbarre']
         self.shapeLbarre = d['shapeLbarre']
         self.Lbarres = d['Lbarres']
         self.rowLbarres = d['rowLbarres']
         self.colLbarres = d['colLbarres']
         self.shapeLbarres = d['self.shapeLbarres']
         self.alphabar = d['alphabar']
         self.mubarre = d['mubarre']
         self.Xbarre = d['Xbarre']
         self.gamma = d['gamma']
         self.beta = d['beta']
         self.q = d['q']
         self.qprime = d['qprime']



    def __reduce__(self):
        '''Define how instances of
        `Struct_multires_Lbarre` are pickled.'''
        d=dict()
        d['Lbarre'] = np.asarray(self.Lbarre)
        d['rowLbarre'] = np.asarray(self.rowLbarre)
        d['colLbarre'] = np.asarray(self.colLbarre)
        d['shapeLbarre'] = self.shapeLbarre
        d['Lbarres'] = np.asarray(self.Lbarres)
        d['rowLbarres'] = np.asarray(self.rowLbarres)
        d['colLbarres'] = np.asarray(self.colLbarres)
        d['shapeLbarres'] = self.shapeLbarres
        d['alphabar'] = self.alphabar
        d['mubarre'] = np.asarray(self.mubarre)
        d['Xbarre'] =  np.asarray(self.Xbarre)
        d['gamma'] = self.gamma
        d['beta'] =  self.beta
        d['q'] = self.q
        d['qprime'] = self.qprime
        return (Struct_multires_Lbarre, (d['Lbarre'], d['rowLbarre'], d['colLbarre'], d['shapeLbarre'],
                                         d['Lbarres'], d['rowLbarres'], d['colLbarres'], d['shapeLbarres'],
                                         d['alphabar'], d['mubarre'], d['Xbabarre'], d['gamma'],
                                         d['beta'], d['q'],d['qprime']), d)

cdef class Struct_M_ana_recons:
    """ Class Struct_M_ana_recons
    this class saves Inputs for reconstruction computation
    in its attributes

    - Inputs:

    :param Lambdabarre: Lambdabarre matrix 1d sparse matrix
           matrix whose rows are the nu_xbarre
    :type Lambdabarre: 1d double array
    :param rowla: row array of sparse matrix Lambdabarre
    :type rowla:  1d int_ array
    :param colla: column array of sparse matrix Lambdabarre
    :type colla:  1d int_ array
    :param int shape0la: shape dimension 0 of Lambdabarre matrix
    :param int shape1la: shape dimension 1 of Lambdabarre matrix
    :param Lambdabreve:  Lambdabreve matrix 1d sparse  matrix
           matrix whose rows are the psi_xbreve
    :type Lambdabreve: 1d double array
    :param rowlb: row array of sparse matrix Lambdabreve
    :type rowlb: 1d int_ array
    :param collb: column array of sparse matrix Lambdabreve
    :type collb: 1d int_ array
    :param int shape0lb: shape dimension 0 of Lambdabreve matrix
    :param int shape1lb: shape dimension 1 of Lambdabreve matrix
    :param Reconsbarre: Reconsbarre  matrix 1d sparse matrix
           Reconstruction matrix whose rows are the nu_xbarre
    :type Reconsbarre: 1d double array
    :param rowlra: row array of sparse matrix Reconsbarre
    :type rowlra: 1d int_ array
    :param collra: column array of sparse matrix Reconsbarre
    :type collra: 1d int_ array
    :param int shape0lra: shape dimension 0 of Reconsbarre matrix
    :param int shape1lra: shape dimension 1 of Reconsbarre matrix
    :param Reconsbreve: Reconsbreve  matrix 1d sparse matrix
           Reconstruction matrix matrix whose rows are the psi_xbreve
    :type Reconsbreve: 1d double array
    :param rowlrb: row array of sparse matrix Reconsbreve
    :type rowlrb: 1d int_ array
    :param collrb: column array of sparse matrix Reconsbreve
    :type collrb: 1d int_ array
    :param int shape0lrb: shape dimension 0 of Reconsbreve matrix
    :param int shape1lrb: shape dimension 1 of Reconsbreve matrix

    - Attributes::

    :ivar Lambdabarre: Lambdabarre matrix 1d sparse matrix
          matrix whose rows are the nu_xbarre
    :type Lambdabarre: 1d double array
    :ivar rowLambdabarre: row array of sparse matrix Lambdabarre
    :type rowLambdabarre:  1d int_ array
    :ivar colLambdabarre: column array of sparse matrix Lambdabarre
    :type colLambdabarre:  1d int_ array
    :ivar int shape0Lambdabarre: shape dimension 0 of Lambdabarre matrix
    :ivar int shape1Lambdabarre: shape dimension 1 of Lambdabarre matrix
    :ivar Lambdabreve:  Lambdabreve matrix 1d sparse  matrix
          matrix whose rows are the psi_xbreve
    :type Lambdabreve: 1d double array
    :ivar rowLambdabreve: row array of sparse matrix Lambdabreve
    :type rowLambdabreve: 1d int_ array
    :ivar colLambdabreve: column array of sparse matrix Lambdabreve
    :type colLambdabreve: 1d int_ array
    :ivar int shape0Lambdabreve: shape dimension 0 of Lambdabreve matrix
    :ivar int shape1Lambdabreve: shape dimension 1 of Lambdabreve matrix
    :ivar Reconsbarre: Reconsbarre  matrix 1d sparse matrix
          Reconstruction matrix whose rows are the nu_xbarre
    :type Reconsbarre: 1d double array
    :ivar Recons_row_barre: row array of sparse matrix Reconsbarre
    :type Recons_row_barre: 1d int_ array
    :ivar Recons_col_barre: column array of sparse matrix Reconsbarre
    :type Recons_col_barre: 1d int_ array
    :ivar int Recons_shape0_barre: shape dimension 0 of Reconsbarre matrix
    :ivar int Recons_shape1_barre: shape dimension 1 of Reconsbarre matrix
    :ivar Reconsbreve: Reconsbreve  matrix 1d sparse matrix
          Reconstruction matrix matrix whose rows are the psi_xbreve
    :type Reconsbreve: 1d double array
    :ivar Recons_row_breve: row array of sparse matrix Reconsbreve
    :type Recons_row_breve: 1d int_ array
    :ivar Recons_col_breve: column array of sparse matrix Reconsbreve
    :type Recons_col_breve: 1d int_ array
    :ivar int Recons_shape0_breve: shape dimension 0 of Reconsbreve matrix
    :ivar int Recons_shape1_breve: shape dimension 1 of Reconsbreve matrix

    """
    def __cinit__(self, double[:] Lambdabarre, long int[:] rowla,
                  long  int[:] colla, int shape0la, int shape1la,
                  double[:]  Lambdabreve, long int[:] rowlb,
                  long int[:] collb, int  shape0lb, int  shape1lb,
                  double[:] Reconsbarre, long int[:] rowlra,
                  long int[:] collra, int shape0lra, int shape1lra,
                  double[:] Reconsbreve, long int[:] rowlrb,
                  long int[:] collrb, int shape0lrb, int shape1lrb):
        pass

    def __init__(self, double[:] Lambdabarre, long int[:] rowla,
                 long int[:] colla, int shape0la, int shape1la,
                 double[:]  Lambdabreve, long int[:] rowlb,
                 long int[:] collb, int  shape0lb, int  shape1lb,
                 double[:] Reconsbarre, long int[:] rowlra,
                 long int[:] collra, int shape0lra, int shape1lra,
                 double[:] Reconsbreve, long int[:] rowlrb,
                 long int[:] collrb, int shape0lrb, int shape1lrb):
        self.Lambdabarre = Lambdabarre
        self.rowLambdabarre = rowla
        self.colLambdabarre = colla
        self.shape0Lambdabarre = shape0la
        self.shape1Lambdabarre = shape1la

        self.Lambdabreve = Lambdabreve
        self.rowLambdabreve = rowlb
        self.colLambdabreve = collb
        self.shape0Lambdabreve = shape0lb
        self.shape1Lambdabreve = shape1lb

        self.Reconsbarre = Reconsbarre
        self.Recons_col_barre = collra
        self.Recons_row_barre = rowlra
        self.Recons_shape0_barre = shape0lra
        self.Recons_shape1_barre = shape1lra

        self.Reconsbreve = Reconsbreve
        self.Recons_col_breve = collrb
        self.Recons_row_breve = rowlrb
        self.Recons_shape0_breve = shape0lrb
        self.Recons_shape1_breve = shape1lrb

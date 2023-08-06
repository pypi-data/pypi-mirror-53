# Python modules
from __future__ import division
import math
import pdb
import pprint
from unittest import signals
pp=pprint.pprint

# 3rd party modules
import numpy as np
import scipy.linalg
import scipy.sparse.linalg

# Our modules


MAX_SINGULAR_VALUES = 50

RADIANS_TO_DEGREES = 180 / 3.1415926


# Complex LAPACK functions
zgelss, = scipy.linalg.lapack.get_lapack_funcs( ['gelss'], 
                                                np.array([1j])
                                              )


def hlsvd(signals, nsv_sought, hankel_size, dwell_time):

    if nsv_sought > MAX_SINGULAR_VALUES:
        nsv_sought = MAX_SINGULAR_VALUES        # needed for work matrix compute

    K = nsv_sought
    M = hankel_size
    N = len(signals)

    L = N - M - 1

    X = scipy.linalg.hankel(signals[:L + 1], signals[L:])
    
    U, s, Vh = scipy.sparse.linalg.svds(X, k=K)
    Uk = np.mat(U[:, :K])     # Uk   - truncated matrix U, rank K
    Ubot = Uk[:-1]            # Ubot - Uk after bottom row removed
    Utop = Uk[1:]             # Utop - Uk after top row removed

    zprime, resid, rank, ss = scipy.linalg.lstsq(Ubot, Utop)

    # Diagonalization of zprime yields 'signal'poles' aka 'roots'
    roots = scipy.linalg.eigvals(zprime)

    # Eigenvalues are returned unordered. I sort them here 
    roots = np.array(sorted(roots))

    # Calculation of dampings, freqs, ampls and phases from roots
    # ===============================================================

    dampings    = np.log(np.abs(roots))
    frequencies = np.arctan2(roots.imag, roots.real) / (math.pi * 2.0)

    # Calculation of complex-valued amplitudes , using the 
    # pseudoinverse of the Lrow*kfit Vandermonde matrix zeta.
    # ===============================================================

    #  First calculate zeta:
    zeta = _vanmon(len(signals), roots)

    # zgells writes solution in space of vector x,
    # but the vector 'signal' is preserved. 
    # 5-8-99: rcond was -1.0; g77 makes rank = 0!! Not with SUN.
    #         So I set rcond = +1.0d-10!!!!

    lwork = 2*MAX_SINGULAR_VALUES+64*(len(signals)+MAX_SINGULAR_VALUES)

    v, x, s, rank, _, info = zgelss(zeta, signals, cond=-1.0, lwork=lwork,
                                    overwrite_a=False, overwrite_b=False)

    # FIXME this code, like the Fortran, ignores possible errors reported 
    # in the "info" return value.

    # Discard the unneeded values of x.
    x = x[:K]
    amplitudes = np.abs(x)
    phases     = np.arctan2(x.imag, x.real)
    
    # convert to values used in Vespa-Analysis

    damping_factors = [1 / df for df in dampings]
    damping_factors = [df * dwell_time for df in damping_factors]

    frequencies = [frequency / dwell_time for frequency in frequencies]

    phases = [phase * RADIANS_TO_DEGREES for phase in phases]

    return (nsv_sought, s, frequencies, damping_factors, amplitudes, phases)




def _vanmon(n_data_points, roots):
    """ calculates the ndp*kfit Vandermonde matrix zeta. """

    nsv_found = len(roots)

    zeta = np.zeros( (n_data_points, nsv_found), np.complex128)

    zeta[1, :nsv_found] = (1+0j)

    for j in range(nsv_found):
        root = roots[j]
        #print "vanmon, roots[{}] = {:.17E}".format(j + 1, root)
        temp = (1+0j)
        for i in range(1, n_data_points):
            temp *= root
            zeta[i, j] = temp
            #print "zeta[{},{}] = {:.17E}".format(i + 1, j + 1, temp)

    return zeta


def _zcalc(nsv_found, n_rows, uuu):
    # c=======================================================================
    #       subroutine Zcalc(kfit,kmax,Lrow,U,zprime,us,unit)

    # PS - zprime is the output of this function
    # PS - unit is only used in this function
    # PS - us is only used in this function

    uuu_sum = np.zeros( (nsv_found, nsv_found), np.complex128)

    m = n_rows

    for i in range(nsv_found):
        for j in range(nsv_found):
            # PS This is the Fortran equivalent, but slow --
            # sum_ = (0+0j)
            # for k in range(m - 1):
            #     sum_ += uuu[k][i].conjugate() * uuu[k + 1][j]

            # PS - This is the fast way to do the same --
            # FIXME - is there an off by one error here? Double check sums
            # against Fortran.
            sum_ = (uuu[:m - 1, i].conjugate() * uuu[1:m, j]).sum()

            uuu_sum[i][j] = sum_



    # PS this is the simple Python equivalent of the fortran loop --
    # sum_ = (0+0j)
    # for i in range(kfit):
    #     sum_ += uuu[m - 1, i].conjugate() * uuu[m - 1, i]

    # Here's the fast way to do it -- 
    sum_ = (uuu[m - 1, :nsv_found].conjugate() * uuu[m - 1, :nsv_found]).sum()

    uot = 1.0 - sum_.real

    unit = np.zeros( (nsv_found, nsv_found), np.complex128)

    for i in range(nsv_found):
        for j in range(nsv_found):
            temp = ((1+0j) if j == i else (0+0j))
            unit[i, j] = temp + (uuu[m - 1][i].conjugate() * uuu[m - 1][j] / uot)
            #print "unit({}, {}) = {:.17E}".format(i + 1, j + 1, unit[i, j])


    zprime = np.zeros( (nsv_found, nsv_found), np.complex128)

    for i in range(nsv_found):
        for j in range(nsv_found):
            zprime[i, j] = (unit[i, :nsv_found] * uuu_sum[:nsv_found, j]).sum()

    return zprime

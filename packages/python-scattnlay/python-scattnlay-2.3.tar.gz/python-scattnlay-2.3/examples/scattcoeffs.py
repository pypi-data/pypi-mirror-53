#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#    Copyright (C) 2009-2015 Ovidio Peña Rodríguez <ovidio@bytesfall.com>
#
#    This file is part of python-scattnlay
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    The only additional remark is that we expect that all publications
#    describing work using this software, or all commercial products
#    using it, cite the following reference:
#    [1] O. Pena and U. Pal, "Scattering of electromagnetic radiation by
#        a multilayered sphere," Computer Physics Communications,
#        vol. 180, Nov. 2009, pp. 2348-2354.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This is a test against the program n-mie (version 3a) for the test case
# distributed by them (extended for x up to 100)
# n-mie is based in the algorithm described in:
# Wu Z.P., Wang Y.P.
# Electromagnetic scattering for multilayered spheres:
# recursive algorithms
# Radio Science 1991. V. 26. P. 1393-1401.
# Voshchinnikov N.V., Mathis J.S.
# Calculating Cross Sections of Composite Interstellar Grains
# Astrophys. J. 1999. V. 526. #1. 

# The test consist in 5 layers with the following parameters
# m1=1.8 i1.7
# m2=0.8 i0.7
# m3=1.2 i0.09
# m4=2.8 i0.2
# m5=1.5 i0.4

# v1/Vt=0.1
# v2/Vt=0.26
# v3/Vt=0.044
# v4/Vt=0.3666

from scattnlay import scattcoeffs
import numpy as np

#import example

size = np.arange(0.25, 100.25, 0.25)

x = np.vstack(( 0.1**(1.0/3.0)*size,
                0.36**(1.0/3.0)*size,
                0.404**(1.0/3.0)*size,
                0.7706**(1.0/3.0)*size,
                size)).transpose()

m = np.array((1.8 + 1.7j, 0.8 + 0.7j, 1.2 + 0.09j,
              2.8 + 0.2j, 1.5 + 0.4j), dtype = np.complex128)

# for i in range(300):
#     terms, an, bn = scattcoeffs(x, m, 105)
nmax=105
an2 = np.zeros((len(size),nmax), dtype = np.complex128)
bn2 = np.zeros((len(size),nmax), dtype = np.complex128)

for _ in range(300):
    for i in range(len(size)):
        terms1, an2[i,:], bn2[i,:] = scattcoeffs(x[i,:], m, nmax=nmax)

# print(an1[:3], bn1[:3])
# print(an2)
# print(an)
# print(terms1)

# result = np.vstack((x[:, 4], an[:, 0].real, an[:, 0].imag, an[:, 1].real, an[:, 1].imag, an[:, 2].real, an[:, 2].imag,
#                              bn[:, 0].real, bn[:, 0].imag, bn[:, 1].real, bn[:, 1].imag, bn[:, 2].real, bn[:, 2].imag)).transpose()

# try:
#     import matplotlib.pyplot as plt

#     plt.figure(1)
#     for i in range(3):
#         plt.subplot(310 + i + 1)
#         plt.plot(x[:, 4], an[:, i].real, label = "Re(a$_%i$)" % (i + 1))
#         plt.plot(x[:, 4], bn[:, i].real, label = "Re(b$_%i$)" % (i + 1))
#         plt.plot(x[:, 4], an[:, i].imag, label = "Im(a$_%i$)" % (i + 1))
#         plt.plot(x[:, 4], bn[:, i].imag, label = "Im(b$_%i$)" % (i + 1))

#         plt.ylabel('n = %i' % (i + 1))
#         plt.legend()

#     plt.xlabel('X')
    
#     plt.show()
# finally:
#     np.savetxt("scattcoeffs.txt", result, fmt = "%.5f")
#     print( result[0,:])


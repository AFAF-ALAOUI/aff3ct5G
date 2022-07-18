#!/usr/bin/env python3

import sys
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location
import py_aff3ct

from py_aff3ct.module.py_module import Py_Module

import numpy as np
import math

import matplotlib.pyplot as plt
from matplotlib import colors

from DMRS_functions import *

class Ressource_allocater(Py_Module):

    def allocate(self, In, Out, Na, Mgrid, M, Data_fPos, DMRS_Pos):

        Grid = np.zeros(shape=(Na,Mgrid), dtype = np.complex64)
        #DMRS = np.reshape(InD[0,0::2]+1j*InD[0,1::2], (Na,M_DMRS//(2*Na)))
        I = np.reshape(In[0,0::2]+1j*In[0,1::2], (Na,M//(2*Na)))
        Grid[:,Data_fPos[:M//(2*Na)]] = I[:,:]

        #Grid[:,DMRS_Pos] = DMRS[:,:]

        Out[0, ::2] = np.real(np.reshape(Grid,(1, Mgrid*Na)))
        Out[0, 1::2] = np.imag(np.reshape(Grid,(1, Mgrid*Na)))


        return 0

    def extract(self, In, Out, Na, Nr, Mgrid, M, Data_fPos, DMRS_Pos):

        #DMRS = np.zeros(shape=(Nr, M_DMRS//(2*Na)), dtype = np.complex64)
        data = np.zeros(shape=(Nr, M//(2*Na)), dtype = np.complex64)

        I = np.reshape(In[0,0::2]+1j*In[0,1::2], (Nr,Mgrid))
        #DMRS[:] = I[:,DMRS_Pos]
        data[:,:] = I[:,Data_fPos[:M//(2*Na)]]
        Out[0, ::2] = np.real(np.reshape(data,(1,Nr*M//(2*Na))))
        Out[0, 1::2] = np.imag(np.reshape(data,(1,Nr*M//(2*Na))))
        #OutD[0, ::2] = np.real(np.reshape(DMRS,(1,Nr*M_DMRS//(2*Na))))
        #OutD[0, 1::2] = np.imag(np.reshape(DMRS,(1,Nr*M_DMRS//(2*Na))))

        return 0

    def __init__(self, M, Mgrid, Na, Nr, Data_fPos, DMRS_Pos):
        Py_Module.__init__(self)

        self.name = "Allocater"                  # module's name
        task = self.create_task("allocate")       # module's task

        In = self.create_socket_in(task, "B_N", M ,np.float32)
        #InD = self.create_socket_in(task, "D_N", M_DMRS ,np.float32)
        Outt = self.create_socket_out(task, "S_N", 2*Mgrid*Na ,np.float32)
        self.create_codelet(task, lambda slf,lsk,fid: slf.allocate(lsk[In],lsk[Outt], Na, Mgrid, M, Data_fPos, DMRS_Pos))

        task = self.create_task("extract")   # module's task

        I = self.create_socket_in(task, "S_N", 2*Mgrid*Nr ,np.float32)
        Out = self.create_socket_out(task, "B_N", M//Na*Nr ,np.float32)
        #OutD = self.create_socket_out(task, "D_N", M_DMRS//Na*Nr ,np.float32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.extract(lsk[I], lsk[Out], Na, Nr, Mgrid, M, Data_fPos, DMRS_Pos))

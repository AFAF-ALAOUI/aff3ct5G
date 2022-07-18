#!/usr/bin/env python3

import sys
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location
import py_aff3ct

from py_aff3ct.module.py_module import Py_Module

import numpy as np
import math

class Mapper(Py_Module):

    def map(self, In, Out, Nb, Nl):

        P = np.transpose(np.reshape(In[0, ::2]+ 1j*In[0, 1::2], (Nb//(2*Nl), Nl)))
        Out[0, ::2] = np.real(np.reshape(P, (1,Nb//2)))
        Out[0, 1::2] = np.imag(np.reshape(P, (1,Nb//2)))

        return 0

    def demap(self, In, Out, Nb, Nl):

        P = np.reshape(In[0, ::2]+ 1j*In[0, 1::2], (Nl, Nb//(2*Nl)))

        Out[0, ::2] = np.real(np.reshape(np.transpose(P), (1,Nb//2)))
        Out[0, 1::2] = np.imag(np.reshape(np.transpose(P), (1,Nb//2)))

        return 0

    def __init__(self, Nb, Nl):
        Py_Module.__init__(self)

        self.name = "LayerMapper"                  # module's name
        task = self.create_task("map")   # module's task

        In = self.create_socket_in(task, "U_K1", Nb ,np.float32)
        Out = self.create_socket_out(task, "U_K2", Nb ,np.float32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.map(lsk[In], lsk[Out], Nb, Nl))

        task = self.create_task("demap")   # module's task

        In = self.create_socket_in(task, "V_K1", Nb ,np.float32)
        Out = self.create_socket_out(task, "V_K2", Nb ,np.float32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.demap(lsk[In], lsk[Out], Nb, Nl))

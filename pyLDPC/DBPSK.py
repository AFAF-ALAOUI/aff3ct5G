#!/usr/bin/env python3

import sys
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location
import py_aff3ct

from py_aff3ct.module.py_module import Py_Module

import numpy as np
import math

class Modulater(Py_Module):


    def modulate(self, In, Out, A):
        Out[0,:] = In[0,:]*np.concatenate((np.tile([1,1,-1,1], math.floor(A/4)),[1,1,-1,1][:A%4]))

        return 0

    def demodulate(self, In, Out, A):
        Out[0,:] = In[0,:]*np.concatenate((np.tile([1,1,-1,1], math.floor(A/4)),[1,1,-1,1][:A%4]))

        return 0

    def __init__(self, A):
        Py_Module.__init__(self)

        self.name = "pi2Modulater"            # module's name
        task = self.create_task("pimodulate")   # module's task

        In = self.create_socket_in(task, "U_K1", A ,np.float32)
        Out = self.create_socket_out(task, "U_K2", A ,np.float32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.modulate(lsk[In], lsk[Out], A))

        task = self.create_task("pidemodulate")   # module's task

        In = self.create_socket_in(task, "U_K2", A ,np.float32)
        Out = self.create_socket_out(task, "U_K1", A ,np.float32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.modulate(lsk[In], lsk[Out], A))

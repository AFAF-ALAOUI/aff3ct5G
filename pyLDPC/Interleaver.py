#!/usr/bin/env python3

import sys
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location
import py_aff3ct

from py_aff3ct.module.py_module import Py_Module

import numpy as np
import math

class Interleaver(Py_Module):

    def interleave(self, In, Out, E1, E2, f, Qm, C, G):
        Out[0,:f*E1] = np.reshape(In[:f,self.tabE1], (1,f*E1))
        Out[0,f*E1:G] = np.reshape(In[f:,self.tabE2],(1,G-f*E1))

        """for c in range(C):
            pt = E1 if (c < f) else E2
            Out[0, c*pt:(c+1)*pt] = np.reshape(np.transpose(np.reshape(In[c,:pt], (Qm, pt//Qm))),(1,pt))"""
        return 0

    def deinterleave(self, In, Out, E1, E2, f, Qm, C,G):

        Out[:f,self.tabE1] = np.reshape(In[0,:f*E1], (f,E1))
        Out[f:,self.tabE2] = np.reshape(In[0,f*E1:G],(C-f,E2))
        """for c in range(C):
            pt = E1 if (c < f) else E2
            Out[c, :pt] = np.reshape(np.transpose(np.reshape(In[0,c*pt:(c+1)*pt], (pt//Qm, Qm))),(1,pt))"""
        return 0

    def __init__(self, E1, E2, f, Qm, G, C):
        Py_Module.__init__(self)

        self.tabE1 = [i*E1//Qm+j for j in range(E1//Qm) for i in range(Qm)]
        self.tabE2 = [i*E2//Qm+j for j in range(E2//Qm) for i in range(Qm)]

        self.name = "Interleaver"               # module's name
        task = self.create_task("interleave")   # module's task

        In = self.create_socket_in(task, "U_K", E2 ,np.int32)
        Out = self.create_socket_out(task, "itl", G ,np.int32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.interleave(lsk[In], lsk[Out], E1, E2, f, Qm, C, G))

        task = self.create_task("deinterleave")   # module's task

        In = self.create_socket_in(task, "itl", G ,np.int32)
        Out = self.create_socket_out(task, "U_K", E2 ,np.int32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.deinterleave(lsk[In], lsk[Out], E1, E2, f, Qm, C,G))

        task = self.create_task("deinterleaveLLR")   # module's task

        In = self.create_socket_in(task, "itl", G ,np.float32)
        Out = self.create_socket_out(task, "U_K", E2 ,np.float32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.deinterleave(lsk[In], lsk[Out], E1, E2, f, Qm, C,G))

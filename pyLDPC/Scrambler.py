#!/usr/bin/env python3

import sys
sys.path.insert(0, '../../build/lib')
import py_aff3ct

from py_aff3ct.module.py_module import Py_Module

import numpy as np

class Scrambler(Py_Module):

    def Goldseq31(N,c_init):
        Nc = 1600
        X = np.zeros(shape=(1,N+Nc), dtype=np.int32)
        Y = np.zeros(shape=(1,N+Nc), dtype=np.int32)
        X[0,0] = 1
        Y[0,len(bin(c_init))-2-1::-1] = [int(digit) for digit in bin(c_init).replace("0b", "")]

        for j in range(Nc+N-31):
            X[0,j+31] = (X[0,j+3]+X[0,j])%2
            Y[0,j+31] = (Y[0,j+3]+Y[0,j+2]+Y[0,j+1]+Y[0,j])%2

        seq = (X[0,Nc:Nc+N]+Y[0,Nc:Nc+N])%2
        return seq

    def scramble(self, In, Out, seq):
        Out[0,:] = (In[0,:] + seq)%2

        return 0

    def descramble(self, In, Out, seq):
        Out[0,:] = (In[0,:] + seq)%2
        return 0

    def descrambleLLR(self, In, Out, seq):
        Out[0,:] = In[0,:]*(1 - 2*seq)
        return 0


    def __init__(self, G, seq):
        Py_Module.__init__(self)

        self.name = "Scrambler"                  # module's name
        task = self.create_task("scramble")   # module's task

        In = self.create_socket_in(task, "S_K1", G ,np.int32)
        Out = self.create_socket_out(task, "S_K2", G ,np.int32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.scramble(lsk[In], lsk[Out], seq))

        task = self.create_task("descramble")   # module's task

        In = self.create_socket_in(task, "S_K2", G ,np.int32)
        Out = self.create_socket_out(task, "S_K1", G ,np.int32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.descramble(lsk[In], lsk[Out], seq))

        task = self.create_task("descrambleLLR")   # module's task

        In = self.create_socket_in(task, "S_K2", G ,np.float32)
        Out = self.create_socket_out(task, "S_K1", G ,np.float32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.descrambleLLR(lsk[In], lsk[Out], seq))

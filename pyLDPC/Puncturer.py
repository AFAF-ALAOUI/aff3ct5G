#!/usr/bin/env python3

import sys
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location
import py_aff3ct

from py_aff3ct.module.py_module import Py_Module

import numpy as np
import math

class Puncturer(Py_Module):

    def index_Table(self, E2, Kp, K, N, Zc, stp):
        tab = [0]*E2
        k = 0
        j= 0
        while(k < E2):
            if not((stp+j)%(N-2*Zc) + 2*Zc < K and Kp <=(stp+j)%(N-2*Zc) + 2*Zc):
                tab[k] = (stp+j)%(N-2*Zc) + 2*Zc
                k+=1

            j+=1
        return tab

    def puncture(self, In, Out, f, E1):
        Out[:f,:E1] = In[:f,self.tabE1]
        Out[f:,:] = In[f:,self.tabE2]
        return 0

    def recover(self, In, Out, f , E1, E2):
        Out[:f,self.tabE1] = In[:f,:E1]
        Out[f:,self.tabE2] = In[f:,:E2]
        return 0

    def recoverLLR(self, In, Out, f , E1, E2, Kp, K, Zc):
        Out[:f,self.tabE1] = In[:f,:E1]
        Out[f:,self.tabE2] = In[f:,:E2]

        Out[:,:2*Zc] = 0
        Out[:,Kp:K] = 1000.00
        return 0


    def __init__(self, Kp, K, N, E1, E2, f, Zc, stp):
        Py_Module.__init__(self)

        Blist = self.index_Table(E2,Kp, K, N, Zc, stp)
        self.tabE1 = Blist[:E1] if (E1 <=  len(Blist)) else np.concatenate((np.tile(Blist,math.floor(E1/len(Blist))),Blist[:E1%len(Blist)]))
        self.tabE2 = Blist[:E2] if (E2 <=  len(Blist)) else np.concatenate((np.tile(Blist,math.floor(E2/len(Blist))),Blist[:E2%len(Blist)]))


        self.name = "Puncturer"               # module's name
        task = self.create_task("puncture")   # module's task

        In = self.create_socket_in(task, "D_K", N ,np.int32)
        Out = self.create_socket_out(task, "D", E2 ,np.int32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.puncture(lsk[In], lsk[Out], f, E1))

        task = self.create_task("recover")   # module's task

        In = self.create_socket_in(task, "D", E2 ,np.int32)
        Out = self.create_socket_out(task, "D_K", N ,np.int32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.recover(lsk[In], lsk[Out], f, E1, E2))

        task = self.create_task("recoverLLR")   # module's task

        In = self.create_socket_in(task, "D", E2 ,np.float32)
        Out = self.create_socket_out(task, "D_K", N ,np.float32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.recoverLLR(lsk[In], lsk[Out], f, E1, E2, Kp, K, Zc))

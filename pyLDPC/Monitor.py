#!/usr/bin/env python3

import sys
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location
import py_aff3ct

from py_aff3ct.module.py_module import Py_Module

import numpy as np
import math



class Monitor(Py_Module):

    def check_errors(self, In, InD, Out, N,C):

        for c in range(C):
            s=0
            for j in range(N):
                if (In[c,j]-InD[c,j] > 1e-6) :
                    s+=1

            Out[c,0] = s

        return 0


    def __init__(self, N,C):
        Py_Module.__init__(self)

        self.name = "Monitor"                  # module's name
        task = self.create_task("check_errors")       # module's task

        In = self.create_socket_in(task, "U", N ,np.float32)
        InD = self.create_socket_in(task, "V",N ,np.float32)
        Outt = self.create_socket_out(task, "Error", 1 ,np.int32)
        self.create_codelet(task, lambda slf,lsk,fid: slf.check_errors(lsk[In], lsk[InD], lsk[Outt], N, C))

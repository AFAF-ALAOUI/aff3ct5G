#!/usr/bin/env python3

import sys
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location
import py_aff3ct

from py_aff3ct.module.py_module import Py_Module

import numpy as np

class Source_SEG(Py_Module):

    def generate(self, In, Out, C):
        Out[0,:] = In[0,:]


        return 0


    def __init__(self, A, C):
        Py_Module.__init__(self)

        self.name = "SourceA"                  # module's name
        task = self.create_task("generate")   # module's task

        In = self.create_socket_in(task, "U_K", A ,np.int32)
        Out = self.create_socket_out(task, "V_K", A ,np.int32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.generate(lsk[In], lsk[Out], C))

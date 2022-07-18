#!/usr/bin/env python3

import sys
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location
import py_aff3ct

from py_aff3ct.module.py_module import Py_Module
import numpy as np


class Segmentor(Py_Module):

    def segment(self, In, Out, B, C):
        Out[::] = np.reshape(In[0,:], (C,B//C))
        return 0

    def concatenate(self, In, Out, B, C):
        Out[0,:] = np.reshape(In[:], (1,B))
        return 0


    def __init__(self, B, C):
        Py_Module.__init__(self)
        self.name = "Segmentor"

        task = self.create_task("segment")


        In = self.create_socket_in(task, "B_K",B, np.int32)
        Out = self.create_socket_out(task, "C_K", B//C ,np.int32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.segment(lsk[In], lsk[Out], B, C))

        task = self.create_task("concatenate")

        In = self.create_socket_in(task, "C_K", B//C, np.int32)
        Out = self.create_socket_out(task, "B_K",B ,np.int32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.concatenate(lsk[In], lsk[Out], B, C))

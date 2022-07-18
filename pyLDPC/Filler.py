#!/usr/bin/env python3

import sys
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location
import py_aff3ct

from py_aff3ct.module.py_module import Py_Module
import numpy as np
import math



class Filler(Py_Module):


    def fill(self, In, Out, Kp):
        Out[:,:Kp] = In[:,:Kp]
        return 0

    def shorten(self, In, Out, Kp):
        Out[:] = In[:,:Kp]
        return 0



    def __init__(self, Kp, K):
        Py_Module.__init__(self)
        self.name = "Filler"

        task = self.create_task("fill")

        In = self.create_socket_in(task, "C_K1", Kp, np.int32)
        Out = self.create_socket_out(task, "C_K2", K ,np.int32)


        self.create_codelet(task, lambda slf,lsk,fid: slf.fill(lsk[In], lsk[Out], Kp))

        task = self.create_task("shorten")

        In = self.create_socket_in(task, "C_K2", K, np.int32)
        Out = self.create_socket_out(task, "C_K1", Kp ,np.int32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.shorten(lsk[In], lsk[Out], Kp))

#!/usr/bin/env python3

import sys
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location
import py_aff3ct

from py_aff3ct.module.py_module import Py_Module

import numpy as np
import math

class ofdm_modem(Py_Module):

    def modulate(self, In, Out, Mgrid, Na, Msc, Nifft, k0):

        Symb = np.zeros(shape=(Mgrid*Na// Msc,Nifft), dtype=np.complex64)

        I = np.reshape(In[0, ::2]+ 1j*In[0, 1::2], (Mgrid*Na//Msc , Msc))
        Symb[:, (Nifft-Msc)//2 + k0 : Nifft-((Nifft-Msc)//2 - k0)] = I
        R = np.fft.ifft(np.fft.ifftshift(Symb, axes=1), Nifft, axis=1)

        Out[0, ::2] = np.real(np.reshape(R,(1,Nifft*Mgrid*Na//Msc)))
        Out[0, 1::2] = np.imag(np.reshape(R,(1,Nifft*Mgrid*Na//Msc)))

        return 0


    def demodulate(self, In, Out, Mgrid, Nr, Msc, Nifft, k0):

        I = np.reshape(In[0, ::2]+ 1j*In[0, 1::2], (Mgrid*Nr//Msc , Nifft))
        S = np.fft.fftshift(np.fft.fft(I, Nifft, axis=1), axes=1)
        SS = S[:,(Nifft-Msc)//2 + k0 : Nifft-((Nifft-Msc)//2 - k0)]

        Out[0, ::2] = np.real(np.reshape(SS, (1,Mgrid*Nr)))
        Out[0, 1::2] = np.imag(np.reshape(SS, (1,Mgrid*Nr)))
        return 0


    def __init__(self, Mgrid, Na, Nr, Msc, Nifft, k0):
        Py_Module.__init__(self)

        self.name = "OFDM"                    # module's name
        task = self.create_task("modulate")   # module's task

        In = self.create_socket_in(task, "X_N", 2*Mgrid*Na, np.float32)
        Out = self.create_socket_out(task, "Y_N", 2*Nifft*Mgrid*Na//Msc, np.float32)


        self.create_codelet(task, lambda slf,lsk,fid: slf.modulate(lsk[In], lsk[Out], Mgrid, Na, Msc, Nifft, k0))

        task = self.create_task("demodulate")   # module's task


        In = self.create_socket_in(task, "Y_N", 2*Nifft*Mgrid*Nr//Msc ,np.float32)
        Out = self.create_socket_out(task, "X_N", 2*Mgrid*Nr ,np.float32)


        self.create_codelet(task, lambda slf,lsk,fid: slf.demodulate(lsk[In], lsk[Out], Mgrid, Nr, Msc, Nifft, k0))

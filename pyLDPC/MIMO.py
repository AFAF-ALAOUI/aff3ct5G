#!/usr/bin/env python3

import sys
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location

import py_aff3ct

from py_aff3ct.module.py_module import Py_Module

import numpy as np
import math
import Precoder

class MimoChannel(Py_Module):

    def add_noise(self, In, Out, CP, Hout, Na, Nr, M):

        if (Na==Nr==1):
            Out[0,:]= In[0,:] + CP[0,0]*(np.random.randn(1,M))
            Hout[0,:] = [1]

        else:

            H = np.random.randn(Nr,Na) + 1j* np.random.randn(Nr,Na)
            I = In[0, ::2]+ 1j*In[0, 1::2]
            I = np.reshape(I, (Na,M//2))
            Y = np.dot(H,I) + CP[0,0]/np.sqrt(2)*(np.random.randn(Nr,M//2)+1j*np.random.randn(Nr,M//2))

            Out[0, ::2] = np.real(np.reshape(Y, (1,Nr*M//2)))
            Out[0, 1::2] = np.imag(np.reshape(Y, (1,Nr*M//2)))
            Hout[0, ::2] = np.real(np.reshape(H, (1,Nr*Na)))
            Hout[0, 1::2] = np.imag(np.reshape(H, (1,Nr*Na)))

        return 0

    def dec_ZF(self, In, Out, CP, CPOut, InH, Na, Nr, M):


        if (Na == Nr == 1):
            Out[0,:] = In[0,:]
            CPOut[:] = CP[0,0]
        else:
            H = InH[0, ::2] + 1j*InH[0, 1::2]
            H = np.reshape(H,(Nr,Na))

            Y = In[0, ::2]+ 1j*In[0, 1::2]
            Y = np.reshape(Y,(Nr,M//(2*Nr)))

            Hp = np.linalg.pinv(H)

            I = np.dot(Hp,Y)

            Out[0, ::2] = np.real(np.reshape(I, (1,Na*M//(2*Nr))))
            Out[0, 1::2] = np.imag(np.reshape(I, (1,Na*M//(2*Nr))))
            CPOut[:,0] = CP[0,0]*np.sqrt(np.real(np.trace(np.matrix(Hp)*np.matrix(Hp).getH())))
        return 0

    def dec_SIC(self, In, Out, CP, CPOut, InH, Na, Nr, M):


        if (Na == Nr == 1):
            Out[0,:] = In[0,:]

        else:
            H = InH[0, ::2] + 1j*InH[0, 1::2]
            H = np.reshape(H,(Nr,Na))
            Y = In[0, ::2]+ 1j*In[0, 1::2]
            Y = np.reshape(Y,(Nr,M//(2*Nr)))
            Q,R = np.linalg.qr(H)
            print(Q.shape, R.shape)

            Z = np.dot(np.matrix(Q).getH(),Y)
            print(Z.shape)
            X = np.zeros(shape=Z.shape, dtype=np.complex64)
            S = np.zeros(shape=Z.shape, dtype=np.complex64)

            X[Na-1,:] = Z[Na-1,:]/R[Na-1,Na-1]
            S = np.dot(R,X)
            for n in range(Na-2,-1, -1):
                X[n,:] = (Z[n,:] -S[n,:])/R[n,n]
                S = np.dot(R,X)

            Out[0, ::2] = np.real(np.reshape(X,(1,Na*M//(2*Nr))))
            Out[0, 1::2] = np.imag(np.reshape(X, (1,Na*M//(2*Nr))))

        CPOut[:,0] = CP[0,0]
        return 0

    def __init__(self, Na, Nr, Nl, M, Mn, Type):
        Py_Module.__init__(self)

        self.name = "MIMOChannel"                  # module's name
        task = self.create_task("add_noise")   # module's task

        CP = self.create_socket_in(task, "CP", 1 ,np.float32)
        In = self.create_socket_in(task, "X_N", M*Na ,np.float32)
        Out = self.create_socket_out(task, "Y_N", M*Nr ,np.float32)
        OutH = self.create_socket_out(task, "H", 2*Nr*Na ,np.float32)


        self.create_codelet(task, lambda slf,lsk,fid: slf.add_noise(lsk[In], lsk[Out], lsk[CP], lsk[OutH], Na, Nr, M))

        task = self.create_task("dec")   # module's task

        CP = self.create_socket_in(task, "CP", 1 ,np.float32)
        In = self.create_socket_in(task, "U_K1", Mn ,np.float32)
        Out = self.create_socket_out(task, "U_K2", Mn*Na//Nr,np.float32)
        InH = self.create_socket_in(task, "H", 2*Na*Nr ,np.float32)
        CPOut = self.create_socket_out(task, "CPN", 1 ,np.float32)

        if (Type == "SIC" and Nr >= Na):
            self.create_codelet(task, lambda slf,lsk,fid: slf.dec_SIC(lsk[In], lsk[Out], lsk[CP], lsk[CPOut], lsk[InH], Na, Nr, Mn))
        else:
            self.create_codelet(task, lambda slf,lsk,fid: slf.dec_ZF(lsk[In], lsk[Out], lsk[CP], lsk[CPOut], lsk[InH], Na, Nr, Mn))

import sys
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location
import py_aff3ct


from py_aff3ct.module.py_module import Py_Module

import numpy as np
import math

class Precoder(Py_Module):
    lis_W = [[1/math.sqrt(2)*np.array([[[1],[0]],[[0],[1]], [[1],[1]], [[1],[-1]], [[1],[1j]], [[1],[-1j]]], dtype=np.complex64)],
    [1/2*np.array([[[1],[0],[0],[0]],[[0],[1],[0],[0]],[[0],[0],[1],[0]],[[0],[0],[0],[1]],[[1],[0],[1],[0]],[[1],[0],[-1],[0]],[[1],[0],[1j],[0]],[[1],[0],[-1j],[0]],[[0],[1],[0],[1]],[[0],[1],[0],[-1]],[[0],[1],[0],[1j]],[[0],[1],[0],[-1j]],[[1],[1],[1],[-1]],[[1],[1],[1j],[1j]],[[1],[1],[-1],[1]],[[1],[1],[-1j],[-1j]],[[1],[1j],[1],[1j]],[[1],[1j],[1j],[1]],[[1],[1j],[-1],[-1j]],[[1],[1j],[-1j],[-1]],[[1],[-1],[1],[1]],[[1], [-1],[1j],[-1j]],[[1],[-1],[-1],[-1]],[[1],[-1],[-1j],[1j]],[[1],[-1j],[1],[-1j]],[[1],[-1j],[1j],[-1]],[[1],[-1j],[-1],[1j]],[[1],[-1j],[-1j],[1]]] , dtype=np.complex64)],
    [1/2*np.array([[[1],[0],[0],[0]],[[0],[1],[0],[0]],[[0],[0],[1],[0]],[[0],[0],[0],[1]],[[1],[0],[1],[0]],[[1],[0],[-1],[0]],[[1],[0],[1j],[0]],[[1],[0],[-1j],[0]],[[0],[1],[0],[1]],[[0],[1],[0],[-1]],[[0],[1],[0],[1j]],[[0],[1],[0],[-1j]],[[1],[1],[1],[1]],[[1],[1],[1j],[1j]],[[1],[1],[-1],[-1]],[[1],[1],[-1j],[-1j]],[[1],[1j],[1],[1j]],[[1],[1j],[1j],[-1]],[[1],[1j],[-1],[-1j]],[[1],[1j],[-1j],[1]],[[1],[-1],[1],[-1]],[[1], [-1],[1j],[-1j]],[[1],[-1],[-1],[1]],[[1],[-1],[-1j],[1j]],[[1],[-1j],[1],[-1j]],[[1],[-1j],[1j],[1]],[[1],[-1j],[-1],[1j]],[[1],[-1j],[-1j],[-1]]] , dtype=np.complex64)],
    [np.array([[[1/math.sqrt(2),0],[0,1/math.sqrt(2)]],[[1/2,1/2],[1/2,-1/2]],[[1/2,1/2],[1j/2,-1j/2]]], dtype=np.complex64)],
    [np.array([[[1/2,0],[0,1/2],[0,0],[0,0]],[[1/2,0],[0,0],[0,1/2],[0,0]],[[1/2,0],[0,0],[0,0],[0,1/2]],[[0,0],[1/2,0],[0,1/2],[0,0]],[[0,0],[1/2,0],[0,0],[0,1/2]],[[0,0],[0,0],[1/2,0],[0,1/2]],[[1/2,0],[0,1/2],[1/2,0],[0,-1j/2]],[[1/2,0],[0,1/2],[1/2,0],[0,1j/2]],[[1/2,0],[0,1/2],[-1j/2,0],[0,1/2]],[[1/2,0],[0,1/2],[-1j/2,0],[0,-1/2]],[[1/2,0],[0,1/2],[-1/2,0],[0,-1j/2]],[[1/2,0],[0,1/2],[-1/2,0],[0,1j/2]],[[1/2,0],[0,1/2],[1j/2,0],[0,1/2]],[[1/2,0],[0,1/2],[1j/2,0],[0,-1/2]],[[1/(2*math.sqrt(2)),1/(2*math.sqrt(2))],[1/(2*math.sqrt(2)),1/(2*math.sqrt(2))],[1/(2*math.sqrt(2)),-1/(2*math.sqrt(2))],[1/(2*math.sqrt(2)),-1/(2*math.sqrt(2))]],[[1/(2*math.sqrt(2)),1/(2*math.sqrt(2))],[1/(2*math.sqrt(2)),1/(2*math.sqrt(2))],[1j/(2*math.sqrt(2)),-1j/(2*math.sqrt(2))],[1j/(2*math.sqrt(2)),-1j/(2*math.sqrt(2))]],[[1/(2*math.sqrt(2)),1/(2*math.sqrt(2))],[1j/(2*math.sqrt(2)),1j/(2*math.sqrt(2))],[1/(2*math.sqrt(2)),-1/(2*math.sqrt(2))],[1j/(2*math.sqrt(2)),-1j/(2*math.sqrt(2))]],[[1/(2*math.sqrt(2)),1/(2*math.sqrt(2))],[1j/(2*math.sqrt(2)),1j/(2*math.sqrt(2))],[1j/(2*math.sqrt(2)),-1j/(2*math.sqrt(2))],[-1/(2*math.sqrt(2)),1/(2*math.sqrt(2))]],[[1/(2*math.sqrt(2)),1/(2*math.sqrt(2))],[-1/(2*math.sqrt(2)),-1/(2*math.sqrt(2))],[1/(2*math.sqrt(2)),-1/(2*math.sqrt(2))],[-1/(2*math.sqrt(2)),1/(2*math.sqrt(2))]],[[1/(2*math.sqrt(2)),1/(2*math.sqrt(2))],[-1/(2*math.sqrt(2)),-1/(2*math.sqrt(2))],[1j/(2*math.sqrt(2)),-1j/(2*math.sqrt(2))],[-1j/(2*math.sqrt(2)),1j/(2*math.sqrt(2))]],[[1/(2*math.sqrt(2)),1/(2*math.sqrt(2))],[-1j/(2*math.sqrt(2)),-1j/(2*math.sqrt(2))],[1/(2*math.sqrt(2)),-1/(2*math.sqrt(2))],[-1j/(2*math.sqrt(2)),1j/(2*math.sqrt(2))]],[[1/(2*math.sqrt(2)),1/(2*math.sqrt(2))],[-1j/(2*math.sqrt(2)),-1j/(2*math.sqrt(2))],[1j/(2*math.sqrt(2)),-1j/(2*math.sqrt(2))],[1/(2*math.sqrt(2)),-1/(2*math.sqrt(2))]]],dtype=np.complex64)],
    [np.array([[[1/2,0,0],[0,1/2,0],[0,0,1/2],[0,0,0]],[[1/2,0,0],[0,1/2,0],[1/2,0,0],[0,0,1/2]],[[1/2,0,0],[0,1/2,0],[-1/2,0,0],[0,0,1/2]],[[1/(2*math.sqrt(3)),1/(2*math.sqrt(3)),1/(2*math.sqrt(3))],[1/(2*math.sqrt(3)),-1/(2*math.sqrt(3)),1/(2*math.sqrt(3))], [1/(2*math.sqrt(3)),1/(2*math.sqrt(3)),-1/(2*math.sqrt(3))], [1/(2*math.sqrt(3)),-1/(2*math.sqrt(3)),-1/(2*math.sqrt(3))]],[[1/(2*math.sqrt(3)),1/(2*math.sqrt(3)),1/(2*math.sqrt(3))],[1/(2*math.sqrt(3)),-1/(2*math.sqrt(3)),1/(2*math.sqrt(3))], [1j/(2*math.sqrt(3)),1j/(2*math.sqrt(3)),-1j/(2*math.sqrt(3))], [1j/(2*math.sqrt(3)),-1j/(2*math.sqrt(3)),-1j/(2*math.sqrt(3))]],[[1/(2*math.sqrt(3)),1/(2*math.sqrt(3)),1/(2*math.sqrt(3))],[-1/(2*math.sqrt(3)),1/(2*math.sqrt(3)),-1/(2*math.sqrt(3))], [1/(2*math.sqrt(3)),1/(2*math.sqrt(3)),-1/(2*math.sqrt(3))], [-1/(2*math.sqrt(3)),1/(2*math.sqrt(3)),1/(2*math.sqrt(3))]],[[1/(2*math.sqrt(3)),1/(2*math.sqrt(3)),1/(2*math.sqrt(3))],[-1/(2*math.sqrt(3)),1/(2*math.sqrt(3)),-1/(2*math.sqrt(3))], [1j/(2*math.sqrt(3)),1j/(2*math.sqrt(3)),-1j/(2*math.sqrt(3))], [-1j/(2*math.sqrt(3)),1j/(2*math.sqrt(3)),1j/(2*math.sqrt(3))]]],dtype=np.complex64)],
    [np.array([[[1/2,0,0,0],[0,1/2,0,0],[0,0,1/2,0],[0,0,0,1/2]],[[1/(2*math.sqrt(2)),1/(2*math.sqrt(2)),0,0],[0,0,1/(2*math.sqrt(2)),1/(2*math.sqrt(2))],[1/(2*math.sqrt(2)),-1/(2*math.sqrt(2)),0,0],[0,0,1/(2*math.sqrt(2)),-1/(2*math.sqrt(2))]],[[1/(2*math.sqrt(2)),1/(2*math.sqrt(2)),0,0],[0,0,1/(2*math.sqrt(2)),1/(2*math.sqrt(2))],[1j/(2*math.sqrt(2)),-1j/(2*math.sqrt(2)),0,0],[0,0,1j/(2*math.sqrt(2)),-1j/(2*math.sqrt(2))]],[[1/4,1/4,1/4,1/4],[1/4,-1/4,1/4,-1/4],[1/4,1/4,-1/4,-1/4],[1/4,-1/4,-1/4,1/4]],[[1/4,1/4,1/4,1/4],[1/4,-1/4,1/4,-1/4],[1j/4,1j/4,-1j/4,-1j/4],[1j/4,-1j/4,-1j/4,1j/4]]],dtype=np.complex64)]]

    d = {0:[1,2,0], 1:[1,4,0], 2:[1,4,1], 3:[2,2,0], 4:[2,4,0], 5:[3,4,0], 6:[4,4,0]}

    def precoding_matrix(Nl, Na, TPMI, val):
        W = np.array([1], dtype = np.complex64)
        for key, value in Precoder.d.items():
            if value == list((Nl,Na,val)):
                if (TPMI >= Precoder.lis_W[key][0].shape[0]):
                    print("TPMI is out of range for Nl and Na given", Precoder.lis_W[key][0].shape[0]-1, "will be used instead")
                    TPMI = Precoder.lis_W[key][0].shape[0]-1
                else:
                    W = Precoder.lis_W[key][0][TPMI]
        return W

    def precode(self, In, Out, Nb, Nl, Na, W):

        Out[0,:Nb] = In[0,:]
        if (W.shape[0] != 1):
            I = In[0, ::2]+ 1j*In[0, 1::2]
            P = np.reshape(I, (Nl, Nb//(2*Nl)))

            Out[0, ::2] = np.real(np.reshape(np.dot(W,P), (1,Na*Nb//(2*Nl))))
            Out[0, 1::2] = np.imag(np.reshape(np.dot(W,P), (1,Na*Nb//(2*Nl))))

        return 0

    def decode(self, In, Out, Nb, Nl, Na, W):
        Out[0,:] = In[0,:Nb]
        if (W.shape[0] != 1):
            I = In[0, ::2]+ 1j*In[0, 1::2]
            P = np.reshape(I, (Na, Nb//(2*Nl)))

            Out[0, ::2] = np.real(np.reshape(np.dot(np.linalg.pinv(W),P), (1,Nb//2)))
            Out[0, 1::2] = np.imag(np.reshape(np.dot(np.linalg.pinv(W),P), (1,Nb//2)))

        return 0

    def __init__(self, Nb, Nl, Na, W):
        Py_Module.__init__(self)

        self.name = "Precoder"                  # module's name
        task = self.create_task("precode")   # module's task

        In = self.create_socket_in(task, "U_K1", Nb ,np.float32)
        Out = self.create_socket_out(task, "U_K2", (Nb//Nl)*Na ,np.float32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.precode(lsk[In], lsk[Out], Nb, Nl, Na, W))

        task = self.create_task("decode")   # module's task

        In = self.create_socket_in(task, "V_K1", (Nb//Nl)*Na ,np.float32)
        Out = self.create_socket_out(task, "V_K2", Nb ,np.float32)

        self.create_codelet(task, lambda slf,lsk,fid: slf.decode(lsk[In], lsk[Out], Nb, Nl, Na, W))

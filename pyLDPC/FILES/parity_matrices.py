import sys
sys.path.insert(0, '../../../build/lib') # pyaf location
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location
import py_aff3ct
import pyaf
import numpy as np
import galois
import os

GF = galois.GF(2)

for BG in range(1,3):
    for Zc in [384]:

        ils = 7*(Zc%15==0) +6*(Zc%13==0) +5*(Zc%11==0) +4*(Zc%9==0) +3*(Zc%7==0) +2*(Zc%5==0 and Zc%15!=0) +(Zc%3==0 and Zc%9!=0 and Zc%15!=0)

        K = 22 if (BG==1) else 10
        N = 68 if (BG==1) else 52
        H = py_aff3ct.tools.sparse_matrix.qc.read("./base_matrices/NR_"+str(BG)+"_"+str(ils)+"_"+str(Zc)+".qc")

        H = np.transpose(np.array(H.full(), dtype=np.int32))
        u = np.zeros(Zc, dtype=np.int32)
        G = np.ones(shape=(Zc*K,Zc*(N-K)), dtype=np.int32)
        u[0]=1

        D = H[:,K*Zc:]
    
        Dp = np.diag(np.linalg.pinv(GF(D)))

        for j in range(K):
            print(j)
            G[j*Zc,:] = np.dot(GF(Dp), np.dot(GF(H[:,j*Zc:(j+1)*Zc]),GF(np.transpose(u))))


        """for i in range(1,Zc):
                for k in range((N-K)):
                    G[j*Zc+i,k*Zc:(k+1)*Zc] = np.concatenate(([G[j*Zc+(i-1),(k+1)*Zc-1]],G[j*Zc+(i-1),k*Zc:(k+1)*Zc-1]),axis=0)


        GG = np.concatenate((np.eye(K*Zc, dtype=np.int32),G),axis=1)


        PP =np.dot(GF(H),np.transpose(GF(GG)))


        for j in range((N-K)*Zc):
            print(PP[j,:])"""


        np.savetxt("gen_matrices/NR_"+str(BG)+"_"+str(ils)+"_"+str(Zc)+".txt", G[::Zc,:])

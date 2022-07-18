import sys
sys.path.insert(0, '../../../build/lib') # pyaf location
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location
import py_aff3ct
import pyaf


import OFDM
import Scrambler
import Precoder
import MIMO
import Allocater

from DMRS_functions import *
from TransBlockSize import *
import argparse
import os
import matplotlib
import matplotlib.pyplot as plt
import time
import numpy as np
import math

parser = argparse.ArgumentParser()
parser.add_argument("-A",   help = "Input Frame Length", type=int)
parser.add_argument("-MCS", help = "Encoding Rate and Modulation Order", type=int, default=0)
parser.add_argument("-I",   help = "LDPC Iteration number", type=int, default=10)
parser.add_argument("-rv",   help = "Redundancy Version",   type=int, choices=[0,1,2,3], default=0)
parser.add_argument("-Nl",  help = "Number of layers",      type=int  , choices=[1,2,3,4],   default=1)
parser.add_argument("-Na",  help = "Number of antennas",    type=int  , choices=[1,2,4],     default=1)
parser.add_argument("-Nr",  help = "Number of rantennas",    type=int  ,  default=1)
parser.add_argument("-nID", help = "Sequence initializing", type=int  , choices=[0,1], default=1)
parser.add_argument("-nRA", help = "Sequence initializing", type=int  , choices=[0,1], default=1)
parser.add_argument("-nRN", help = "Sequence initializing", type=int  , choices=[0,1], default=1)
parser.add_argument("-pi2", help = "pi2_BPSK flag",  type=int  , choices=[0,1],  default=0)
parser.add_argument("-TPMI",help = "Precoding matrix Index",type=int  , default=0)
parser.add_argument("-val", help = "Transform precoding state" ,type=int , choices=[0,1]  ,default=0)
parser.add_argument("-Cf",  help = "Configuration Type" ,  type=int , choices=[1,2]  ,default=1)
parser.add_argument("-Mp",  help = "Mapping Type" ,  type=str , choices=['A','B']  ,default='A')
parser.add_argument("-Dl",  help = "DMRS Length" ,  type=int , choices=[1,2]  ,default=1)
parser.add_argument("-Fh",  help = "Frequency hopping flag" ,  type=int , choices=[0,1]  ,default=0)
parser.add_argument("-pos", help = "DMRS first position" ,  type=int, default=2)
parser.add_argument("-apos",help = "DMRS additional position" , type=int, choices=[0,1,2,3], default=0)
parser.add_argument("-Sd",  help = "PUSCH symbol duration" , type=int, default=14)
parser.add_argument("-mu",  help = "OFDM spacing configuration",type=int , choices=[0,1,2,3,4] ,default=0)
parser.add_argument("-NID", help = "Initialization parameter",type=int ,default=10)
parser.add_argument("-nscid", help = "Initialization parameter",type=int, choices=[0,1], default=1)
parser.add_argument("-CP",    help = "Cyclic prefix conf",type=int, choices=[0,1], default=0)


args = parser.parse_args()

TAB = TAB5_1
L = 24
Kcb = (8448,3840)
Zc_table = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,50,32,36,40,44,48,52,56,60,
64,72,80,88,96,104,112,120,128,144,160,176,192,208,224,240,256,288,320,352,384]

CRC24A = ("0x1864CFB", 24)
CRC24B = ("0x1800063", 24)
CRC24C = ("0x1B2B117", 24)
CRC16  = ("0x11021", 16)
CRC11  = ("0xE21", 11)
CRC6   = ("0x61", 6)
Type   = "ZF"
# parameters
poly_key = CRC24A if(args.A>3824) else CRC16
B   = args.A+24 if(args.A>3824) else args.A+16
R   = TAB[args.MCS][1]/1024
Qm  = TAB[args.MCS][0]
BG  = 1 if (args.A<=292 or (args.A<=3824 and R<=0.67) or R<=0.25) else 0
C   = math.ceil(B/(Kcb[BG]-L)) if (B > Kcb[BG]) else 1
Kp  = math.ceil(B/C)+24 if (C > 1) else B
KB  = 22 if (BG==0) else (10*(B>640) + 9*(B<=640 and B>560 )+ 8*(B<=560 and B>192) + 6*(B<=192))
Zc  = [i for i in Zc_table if KB*i >= Kp][0]
K   = 22*Zc if BG==0  else 10*Zc
N   = 68*Zc if BG==0  else 52*Zc
Np  = N - 2*Zc

CP  = 1 if (args.mu== 2 and args.CP==1) else 0
Mrb = 10
Msc = 12*Mrb
Nofdms = 14
Nslot = 10*2**(args.mu)
Mgrid = Nslot*Nofdms*Msc
k0  = 0
Nifft = 2**(math.ceil(math.log2(Msc+abs(k0))))
LCP = Nifft//4 if CP==1 else 9*Nifft//128

ils = 7*(Zc%15==0) +6*(Zc%13==0) +5*(Zc%11==0) +4*(Zc%9==0) +3*(Zc%7==0) +2*(Zc%5==0 and Zc%15!=0) +(Zc%3==0 and Zc%9!=0 and Zc%15!=0)
G   = args.Nl*Qm * math.floor(C*N/(args.Nl*Qm))
#G   = transportBlocSize(Nofdms, 6, 0, Mrb, R, Qm, args.Nl)

E1   = args.Nl*Qm * math.floor(G/(args.Nl*Qm*C))
E2   = args.Nl*Qm * math.ceil(G/(args.Nl*Qm*C))
f    = int(C - ((G/(args.Nl*Qm))%C))
stp = np.array([[0, math.floor((17*Np)/(66*Zc))*Zc, math.floor((33*Np)/(66*Zc))*Zc, math.floor((56*Np)/(66*Zc))*Zc],
[0, math.floor((13*Np)/(50*Zc))*Zc, math.floor((25*Np)/(50*Zc))*Zc, math.floor((43*Np)/(50*Zc))*Zc]])

c_init = 2**16*args.nRN + 2**10* args.nRA + args.nID



DD = DMRS_TimePosPerSlot(args.Dl, args.Mp,args.Fh,args.pos, args.apos,args.Sd)

sigma = np.ndarray(shape = (1,1),  dtype = np.float32)
sigma[:] = 0.000001


H    = py_aff3ct.tools.sparse_matrix.qc.read("./base_matrices/NR_"+str(BG+1)+"_"+str(ils)+"_"+str(Zc)+".qc")
seq  = Scrambler.Scrambler.Goldseq31(G,c_init)
cstl = py_aff3ct.tools.constellation.Constellation_user("./BPSK/BPSK.mod") if (Qm==1) else py_aff3ct.tools.constellation.Constellation_QAM(Qm)
W    = Precoder.Precoder.precoding_matrix(args.Nl, args.Na, args.TPMI, args.val)


src  = py_aff3ct.module.source.Source_random(args.A)
srca = pyaf.source.Source_SEG(args.A, C)
crc  = py_aff3ct.module.crc.CRC_polynomial(args.A, poly_key[0], poly_key[1])
fill = pyaf.filler.Filler(Kp, K, C)
seg  = pyaf.segmentor.Segmentor(B,C)
rcc  = py_aff3ct.module.crc.CRC_polynomial(B//C, CRC24B[0], CRC24B[1])
enc  = pyaf.encoder.LdpcEncoder_fast(K, N, BG+1, ils, Zc, C)
dec  = py_aff3ct.module.decoder.Decoder_LDPC_BP_horizontal_layered_inter_NMS(K, N, args.I, H, np.arange(K))
pun  = pyaf.puncturer.Puncturer(C, Kp, K, N, E1, E2, f, Zc, stp[BG,args.rv])
itl  = pyaf.interleaver.Row_Column_Interleaver(E1, E2, f, Qm, G, C)
scr  = pyaf.scrambler.Scrambler(G, c_init)
mdm  = py_aff3ct.module.modem.Modem_generic(G, cstl)
shf  = pyaf.pi2modulater.Modulater(2*G//Qm, C)
lmap = pyaf.LayerMapper.Mapper(G//Qm*2, args.Nl, C)
prc  = pyaf.precoder.Precoder(G//Qm*2, args.Nl, args.Na, args.TPMI, args.val)
prc  = Precoder.Precoder(G//Qm*2, args.Nl, args.Na, W)

all  = pyaf.allocater.Allocater(G//(Qm*args.Nl)*2*args.Na, Mgrid, args.Na, args.Nr, Nslot, Nofdms, args.Dl, Msc,*DD)
ofdm = pyaf.ofdm.OfdmModulater(Mgrid , args.Na, args.Nr, Msc, Nifft, k0)
chn  = MIMO.MimoChannel(args.Na, args.Nr, args.Nl, Nifft*2*Mgrid//Msc, G//(Qm*args.Nl)*2*args.Nr, Type)


mnt = py_aff3ct.module.monitor.Monitor_BFER_AR(args.A, 50, 50) if (C==1) else py_aff3ct.module.monitor.Monitor_BFER_AR(B//C, 1, 1)


srca["generate        :: U_K "]  = src["generate         :: U_K "]
crc["build            :: U_K1"]  = srca["generate        :: V_K "]

if (C==1):
    fill["fill            :: C_K1"]  = crc["build            :: U_K2"]
else :
    seg["segment          :: B_K "]  = crc["build            :: U_K2"]
    rcc["build            :: U_K1"]  = seg["segment          :: C_K "]
    fill["fill            :: C_K1"]  = rcc["build            :: U_K2"]


enc["encode           :: U_K "]  = fill["fill            :: C_K2"]
pun["puncture         :: D_K "]  = enc["encode           :: X_N "]
itl["interleave       :: U_K "]  = pun["puncture         :: D   "]
scr["scramble         :: S_K1"]  = itl["interleave       :: itl "]
mdm["modulate         :: X_N1"]  = scr["scramble         :: S_K2"]

if (args.pi2):
    shf["pimodulate      :: U_K1"] = mdm["modulate         :: X_N2"]
    lmap["map            :: U_K1"] = shf["pimodulate       :: U_K2"]
else:
    lmap["map            :: U_K1"] = mdm["modulate         :: X_N2"]

prc["precode          :: U_K1"] = lmap["map            :: U_K2"]
all["allocate         :: B_N "] = prc["precode         :: U_K2"]
ofdm["modulate        :: X_N "] = all["allocate        :: S_N "]
chn["add_noise        :: X_N "] = ofdm["modulate       :: Y_N "]
ofdm["demodulate      :: Y_N "] = chn["add_noise       :: Y_N "]
all["extract          :: S_N "] = ofdm["demodulate     :: X_N "]
chn["dec              :: U_K1"] = all["extract         :: B_N "]
prc["decode           :: V_K1"] = chn["dec             :: U_K2"]
lmap["demap           :: V_K1"] = prc["decode          :: V_K2"]


if (args.pi2):
    shf["pidemodulate    :: U_K2"] = lmap["demap           :: V_K2"]
    mdm["demodulate      :: Y_N1"] = shf["pidemodulate     :: U_K1"]
else:
    mdm["demodulate      :: Y_N1"] = lmap["demap           :: V_K2"]

scr["descrambleLLR    :: S_K2"]  = mdm["demodulate       :: Y_N2"]

itl["deinterleaveLLR  :: itl "]  = scr["descrambleLLR    :: S_K1"]
pun["recoverLLR       :: D   "]  = itl["deinterleaveLLR  :: U_K "]
dec["decode_siho      :: Y_N "]  = pun["recoverLLR       :: D_K "]
fill["shorten         :: C_K2"]  = dec["decode_siho      :: V_K "]

if (C==1):
    crc["extract          :: V_K1"]  = fill["shorten         :: C_K1"]
else :
    rcc["extract          :: V_K1"]  = fill["shorten         :: C_K1"]
    seg["concatenate      :: C_K "]  = rcc["extract          :: V_K2"]
    crc["extract          :: V_K1"]  = seg["concatenate      :: B_K "]

chn["dec              :: H "] = chn["add_noise       :: H  "]
mdm["demodulate       :: CP"] = chn["dec             :: CPN"]
chn["add_noise        :: CP"] = sigma
chn["dec              :: CP"] = sigma


if (C==1):
    mnt["check_errors     :: U"]   = srca["generate       :: V_K"]
    mnt["check_errors     :: V"]   = crc["extract         :: V_K2"]
else:
    mnt["check_errors     :: U"]   = seg["segment          :: C_K "]
    mnt["check_errors     :: V"]   = rcc["extract          :: V_K2"]



py_aff3ct.tools.sequence.Sequence(src["generate"]).set_n_frames(C)
seq = py_aff3ct.tools.sequence.Sequence(src["generate"], 1)
seq.export_dot("seq.dot")




mnt["check_errors"].debug = True
mnt["check_errors"].set_debug_limit(10)

prc["precode"].debug = True
prc["precode"].set_debug_limit(10)


l_tasks = seq.get_tasks_per_types()
for lt in l_tasks:
    for t in lt:
        t.stats = True

seq.exec()


"""
ebn0_min =  -7+args.MCS
ebn0_max =  3+args.MCS
ebn0_step = 0.5

SNR_dB = np.arange(ebn0_min,ebn0_max,ebn0_step)
SNR = 10**(SNR_dB/10)
sigma_vals = 1/np.sqrt(Nifft*SNR*args.Nr)


fer = np.zeros(len(SNR))
ber = np.zeros(len(SNR))

fig = plt.figure()
ax = fig.add_subplot(111)
line1,line2, = ax.semilogy(SNR_dB, fer, 'r-*', SNR_dB, ber, 'b-*',  markerfacecolor='None', markersize=5)
plt.ylim((1e-3, 1.05))



y_major = matplotlib.ticker.LogLocator(base = 10.0, numticks = 10)
ax.yaxis.set_major_locator(y_major)
y_minor = matplotlib.ticker.LogLocator(base = 10.0, subs = np.arange(1.0, 10.0) * 0.1, numticks = 10)
ax.yaxis.set_minor_locator(y_minor)
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())

plt.grid(True, which='both', axis='y')
plt.grid(True, which='major', axis='x')


print("Eb/NO | FRA | BER | FER | Tpt ")
for i in range(len(sigma_vals)):
	sigma[:] = sigma_vals[i]

	t = time.time()
	seq.exec()
	elapsed = time.time() - t
	total_fra = mnt.get_n_analyzed_fra()

	ber[i] = mnt.get_ber()
	fer[i] = mnt.get_fer()

	tpt = total_fra * K * 1e-6/elapsed
	print( SNR_dB[i] ,"|", total_fra, "|", ber[i] ,"|", fer[i] , "|", tpt)

	mnt.reset()

	line1.set_ydata(fer)
	line2.set_ydata(ber)
	fig.canvas.draw()
	fig.canvas.flush_events()
	plt.pause(1e-6)


#np.savetxt('Fig/TBS'+'_R_'+str(R)+'_Qm_'+str(Qm)+'_K_'+str(K)+'_N_'+str(N), (SNR_dB,ber,fer), delimiter=' ', newline=os.linesep)

plt.show()
"""
seq.show_stats()

import sys
sys.path.insert(0, '../../../build/lib') # pyaf location
sys.path.insert(0, '../../../py_aff3ct/build/lib') # py_aff3ct location
import py_aff3ct
import pyaf


import Source
import Filler
import Segmentor
import Puncturer
import Interleaver
import Scrambler
import DBPSK
import LayerMapper
import Allocater
import Precoder
import MIMO
import OFDM

import Monitor

from DMRS_functions import *
from TransBlockSize import *
import argparse
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

TAB = TAB6_1
L = 24
Kcb = (8448,3840)
Zc_table = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20,22,24,26,28,30,32,36,40,44,48,52,56,60,
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

ils = 7*(Zc%15==0) +6*(Zc%13==0) +5*(Zc%11==0) +4*(Zc%9==0) +3*(Zc%7==0) +2*(Zc%5==0 and Zc%15!=0) +(Zc%3==0 and Zc%9!=0 and Zc%15!=0)
G   = args.Nl*Qm * math.floor(C*N/(args.Nl*Qm))

E1   = args.Nl*Qm * math.floor(G/(args.Nl*Qm*C))
E2   = args.Nl*Qm * math.ceil(G/(args.Nl*Qm*C))
f    = int(C - ((G/(args.Nl*Qm))%C))
stp = np.array([[0, math.floor((17*Np)/(66*Zc))*Zc, math.floor((33*Np)/(66*Zc))*Zc, math.floor((56*Np)/(66*Zc))*Zc],
[0, math.floor((13*Np)/(50*Zc))*Zc, math.floor((25*Np)/(50*Zc))*Zc, math.floor((43*Np)/(50*Zc))*Zc]])

c_init = 2**16*args.nRN + 2**10* args.nRA + args.nID

CP  = 1 if (args.mu== 2 and args.CP==1) else 0
Mrb = 1
Msc = 12*Mrb
Nofdms = 14
Nslot = 10*2**(args.mu)
Mgrid = Nslot*Nofdms*Msc
k0  = 0
Nifft = 2**(math.ceil(math.log2(Msc+abs(k0))))
LCP = Nifft//4 if CP==1 else 9*Nifft//128



DMRSTPos = DMRS_TimePos(Nslot,Nofdms, args.Dl, args.Mp,args.Fh,args.pos, args.apos,args.Sd)
DataTPos = Data_TimePos(DMRSTPos,Nslot,Nofdms)
DMRSPos  = DMRS_freqTimePos(DMRSTPos,Msc)
DataPos  = Data_freqPos(DataTPos,Msc)
DD = DMRS_TimePosPerSlot(args.Dl, args.Mp,args.Fh,args.pos, args.apos,args.Sd)

sigma = np.ndarray(shape = (1,1),  dtype = np.float32)
sigma[:] = 0.0001


H    = py_aff3ct.tools.sparse_matrix.qc.read("./base_matrices/NR_"+str(BG+1)+"_"+str(ils)+"_"+str(Zc)+".qc")
seq  = Scrambler.Scrambler.Goldseq31(G,c_init)
cstl = py_aff3ct.tools.constellation.Constellation_user("./BPSK/BPSK.mod") if (Qm==1) else py_aff3ct.tools.constellation.Constellation_QAM(Qm)
W    = Precoder.Precoder.precoding_matrix(args.Nl, args.Na, args.TPMI, args.val)

src  = py_aff3ct.module.source.Source_random(args.A)
srca = Source.Source_SEG(args.A, C)
crc  = py_aff3ct.module.crc.CRC_polynomial(args.A, poly_key[0], poly_key[1])
fill = Filler.Filler(Kp, K)
seg  = Segmentor.Segmentor(B, C)
rcc  = py_aff3ct.module.crc.CRC_polynomial(B//C, CRC24B[0], CRC24B[1])
enc  = py_aff3ct.module.encoder.Encoder_LDPC_from_QC(K, N, H)
dec  = py_aff3ct.module.decoder.Decoder_LDPC_BP_horizontal_layered_inter_NMS(K, N, args.I, H, enc.get_info_bits_pos())
pun  = Puncturer.Puncturer(Kp, K, N, E1, E2, f, Zc, stp[BG,args.rv])
itl  = Interleaver.Interleaver(E1, E2, f, Qm, G, C)
scr  = Scrambler.Scrambler(G, seq)
mdm  = py_aff3ct.module.modem.Modem_generic(G, cstl)
shf  = DBPSK.Modulater(2*G)
lmap = LayerMapper.Mapper(G//Qm*2, args.Nl)
prc  = Precoder.Precoder(G//Qm*2, args.Nl, args.Na, W)
all  = Allocater.Ressource_allocater(G//(Qm*args.Nl)*2*args.Na, Mgrid, args.Na, args.Nr, DataPos, DMRSPos)
ofdm = OFDM.ofdm_modem(Mgrid , args.Na, args.Nr, Msc, Nifft, k0)
chn  = MIMO.MimoChannel(args.Na, args.Nr, args.Nl, Nifft*2*Mgrid//Msc, G//(Qm*args.Nl)*2*args.Nr, Type)



mnt      =  py_aff3ct.module.monitor.Monitor_BFER_AR(args.A, 1, 1)

c_src  = py_aff3ct.module.source.Source_random(args.A)
c_srca = pyaf.source.Source_SEG(args.A, C)
c_crc  = py_aff3ct.module.crc.CRC_polynomial(args.A, poly_key[0], poly_key[1])
c_fill = pyaf.filler.Filler(Kp, K, C)
c_seg  = pyaf.segmentor.Segmentor(B,C)
c_rcc  = py_aff3ct.module.crc.CRC_polynomial(B//C, CRC24B[0], CRC24B[1])
c_enc  = pyaf.encoder.LdpcEncoder(K, N, BG+1, ils, Zc, C)
c_dec  = py_aff3ct.module.decoder.Decoder_LDPC_BP_horizontal_layered_inter_NMS(K, N, args.I, H, np.arange(K))
c_pun  = pyaf.puncturer.Puncturer(C, Kp, K, N, E1, E2, f, Zc, stp[BG,args.rv])
c_itl  = pyaf.interleaver.Row_Column_Interleaver(E1, E2, f, Qm, G, C)
c_scr  = pyaf.scrambler.Scrambler(G, c_init)
c_mdm  = py_aff3ct.module.modem.Modem_generic(G, cstl)
c_lmap = pyaf.LayerMapper.Mapper(G//Qm*2, args.Nl, C)
c_prc  = pyaf.precoder.Precoder(G//Qm*2, args.Nl, args.Na, args.TPMI, args.val)
c_all  = pyaf.allocater.Allocater(G//(Qm*args.Nl)*2*args.Na, Mgrid, args.Na, args.Nr, Nslot, Nofdms, args.Dl, Msc,*DD)
c_ofdm = pyaf.ofdm.OfdmModulater(Mgrid , args.Na, args.Nr, Msc, Nifft, k0)


mntsrc =  py_aff3ct.module.monitor.Monitor_BFER_AR(args.A, 1, 1)
mntseg =  py_aff3ct.module.monitor.Monitor_BFER_AR(B//C, 1, 1)
mntfil =  py_aff3ct.module.monitor.Monitor_BFER_AR(K, 1, 1)
mntenc =  py_aff3ct.module.monitor.Monitor_BFER_AR(N, 1, 1)
mntpun =  py_aff3ct.module.monitor.Monitor_BFER_AR(E2, 1, 1)
mntitl =  py_aff3ct.module.monitor.Monitor_BFER_AR(G, 1, 1)
mntscr =  py_aff3ct.module.monitor.Monitor_BFER_AR(G, 1, 1)
mntmap =  Monitor.Monitor(G//Qm*2,1)
mntall =  Monitor.Monitor(2*Mgrid * args.Na,1)
mntext =  Monitor.Monitor(2*G//(Qm*args.Nl)*args.Nr,1)
mntdem =  Monitor.Monitor(G//Qm*2,1)
mntdsc =  Monitor.Monitor(G,1)
mntdit =  Monitor.Monitor(E2,C)
mntrec =  Monitor.Monitor(N,C)
mntsho =  py_aff3ct.module.monitor.Monitor_BFER_AR(Kp,1,1)
mntcon =  py_aff3ct.module.monitor.Monitor_BFER_AR(B,1,1)
mntofm =  Monitor.Monitor(2*Nifft*Mgrid*args.Na//Msc,1)
mntofd =  Monitor.Monitor(2*Mgrid*args.Nr,1)


srca["generate        :: U_K "]  = src["generate         :: U_K "]
crc["build            :: U_K1"]  = srca["generate        :: V_K "]

c_srca["generate      :: U_K "]  = src["generate         :: U_K "]


if (C==1):
    fill["fill            :: C_K1"]  = crc["build            :: U_K2"]
    c_fill["fill          :: C_K1"]  = crc["build            :: U_K2"]
else :
    seg["segment          :: B_K "]  = crc["build            :: U_K2"]
    rcc["build            :: U_K1"]  = seg["segment          :: C_K "]
    fill["fill            :: C_K1"]  = rcc["build            :: U_K2"]

    c_seg["segment        :: B_K "]  = crc["build            :: U_K2"]
    c_fill["fill          :: C_K1"]  = rcc["build            :: U_K2"]


enc["encode           :: U_K "]  = fill["fill            :: C_K2"]
c_enc["encode         :: U_K "]  = c_fill["fill          :: C_K2"]
pun["puncture         :: D_K "]  = enc["encode           :: X_N "]
c_pun["puncture       :: D_K "]  = c_enc["encode         :: X_N "]
itl["interleave       :: U_K "]  = pun["puncture         :: D   "]
scr["scramble         :: S_K1"]  = itl["interleave       :: itl "]
c_itl["interleave     :: U_K "]  = c_pun["puncture       :: D   "]
c_scr["scramble       :: S_K1"]  = c_itl["interleave     :: itl "]

mdm["modulate         :: X_N1"]  = scr["scramble        :: S_K2"]
lmap["map             :: U_K1"]  = mdm["modulate        :: X_N2"]
c_lmap["map           :: U_K1"]  = mdm["modulate        :: X_N2"]
prc["precode          :: U_K1"]  = lmap["map            :: U_K2"]
c_prc["precode        :: U_K1"]  = lmap["map            :: U_K2"]
all["allocate         :: B_N "]  = prc["precode         :: U_K2"]
c_all["allocate       :: B_N "]  = prc["precode         :: U_K2"]

ofdm["modulate        :: X_N "] = all["allocate        :: S_N "]
c_ofdm["modulate      :: X_N "] = all["allocate        :: S_N "]
chn["add_noise        :: X_N "] = ofdm["modulate       :: Y_N "]
ofdm["demodulate      :: Y_N "] = chn["add_noise       :: Y_N "]
c_ofdm["demodulate    :: Y_N "] = chn["add_noise       :: Y_N "]
all["extract          :: S_N "] = ofdm["demodulate     :: X_N "]
c_all["extract        :: S_N "] = ofdm["demodulate     :: X_N "]
chn["dec              :: U_K1"] = all["extract         :: B_N "]
prc["decode           :: V_K1"] = chn["dec             :: U_K2"]
c_prc["decode         :: V_K1"] = chn["dec             :: U_K2"]
lmap["demap           :: V_K1"] = prc["decode          :: V_K2"]
c_lmap["demap         :: V_K1"] = prc["decode          :: V_K2"]

mdm["demodulate       :: Y_N1"]  = lmap["demap           :: V_K2"]
scr["descrambleLLR    :: S_K2"]  = mdm["demodulate       :: Y_N2"]
itl["deinterleaveLLR  :: itl "]  = scr["descrambleLLR    :: S_K1"]
pun["recoverLLR       :: D   "]  = itl["deinterleaveLLR  :: U_K "]

c_scr["descrambleLLR  :: S_K2"]  = mdm["demodulate       :: Y_N2"]
c_itl["deinterleaveLLR:: itl "]  = c_scr["descrambleLLR  :: S_K1"]
c_pun["recoverLLR     :: D   "]  = c_itl["deinterleaveLLR:: U_K "]

dec["decode_siho      :: Y_N "]  = pun["recoverLLR       :: D_K "]
fill["shorten         :: C_K2"]  = dec["decode_siho      :: V_K "]
c_fill["shorten       :: C_K2"]  = dec["decode_siho      :: V_K "]


if (C==1):
    crc["extract          :: V_K1"]  = fill["shorten         :: C_K1"]
else :
    rcc["extract          :: V_K1"]  = fill["shorten         :: C_K1"]
    seg["concatenate      :: C_K "]  = rcc["extract          :: V_K2"]
    c_seg["concatenate    :: C_K "]  = rcc["extract          :: V_K2"]
    crc["extract          :: V_K1"]  = seg["concatenate      :: B_K "]

chn["dec              :: H "] = chn["add_noise       :: H  "]
mdm["demodulate       :: CP"] = chn["dec             :: CPN"]
chn["add_noise        :: CP"] = sigma
chn["dec              :: CP"] = sigma


mnt["check_errors      :: U"]   = c_srca["generate     :: V_K"]
mnt["check_errors      :: V"]   = crc["extract         ::V_K2"]

mntsrc["check_errors   :: U"]   = c_srca["generate     :: V_K"]
mntsrc["check_errors   :: V"]   = srca["generate       :: V_K"]

mntfil["check_errors   :: U"]   = c_fill["fill         ::C_K2"]
mntfil["check_errors   :: V"]   = fill["fill           ::C_K2"]

mntenc["check_errors   :: U"]   = c_enc["encode        ::X_N"]
mntenc["check_errors   :: V"]   = enc["encode          ::X_N"]

mntseg["check_errors   :: U"]   = c_seg["segment       :: C_K"]
mntseg["check_errors   :: V"]   = seg["segment         :: C_K"]

mntpun["check_errors   :: U"]   = c_pun["puncture      :: D  "]
mntpun["check_errors   :: V"]   = pun["puncture        :: D  "]

mntitl["check_errors   :: U"]   = c_itl["interleave    ::itl "]
mntitl["check_errors   :: V"]   = itl["interleave      ::itl "]

mntscr["check_errors   :: U"]   = c_scr["scramble      ::S_K2"]
mntscr["check_errors   :: V"]   = scr["scramble        ::S_K2"]

mntmap["check_errors   :: U"]   = c_lmap["map          ::U_K2"]
mntmap["check_errors   :: V"]   = lmap["map            ::U_K2"]

mntall["check_errors   :: U"]   = c_all["allocate      ::S_N "]
mntall["check_errors   :: V"]   = all["allocate        ::S_N "]

mntext["check_errors   :: U"]   = c_all["extract       ::B_N "]
mntext["check_errors   :: V"]   = all["extract         ::B_N "]

mntdem["check_errors   :: U"]   = c_lmap["demap        ::V_K2"]
mntdem["check_errors   :: V"]   = lmap["demap          ::V_K2"]

mntdsc["check_errors   :: U"]   = c_scr["descrambleLLR ::S_K1"]
mntdsc["check_errors   :: V"]   = scr["descrambleLLR   ::S_K1"]

mntrec["check_errors   :: U"]   = c_pun["recoverLLR    :: D_K"]
mntrec["check_errors   :: V"]   = pun["recoverLLR      :: D_K"]

mntdit["check_errors   :: U"]   = c_itl["deinterleaveLLR::U_K"]
mntdit["check_errors   :: V"]   = itl["deinterleaveLLR  ::U_K"]

mntsho["check_errors   :: U"]   = c_fill["shorten      ::C_K1"]
mntsho["check_errors   :: V"]   = fill["shorten        ::C_K1"]

mntcon["check_errors   :: U"]   = c_seg["concatenate   ::B_K"]
mntcon["check_errors   :: V"]   = seg["concatenate     ::B_K"]

mntofm["check_errors   :: U"]   = c_ofdm["modulate     :: Y_N "]
mntofm["check_errors   :: V"]   = ofdm["modulate       :: Y_N "]

mntofd["check_errors   :: U"]   = c_ofdm["demodulate    :: X_N "]
mntofd["check_errors   :: V"]   = ofdm["demodulate      :: X_N "]


py_aff3ct.tools.sequence.Sequence(src["generate"]).set_n_frames(C)
seq = py_aff3ct.tools.sequence.Sequence(src["generate"], 1)

mntsrc["check_errors"].debug = True
mntsrc["check_errors"].set_debug_limit(10)

mntseg["check_errors"].debug = True
mntseg["check_errors"].set_debug_limit(10)

mntfil["check_errors"].debug = True
mntfil["check_errors"].set_debug_limit(10)

mntenc["check_errors"].debug = True
mntenc["check_errors"].set_debug_limit(10)

mntpun["check_errors"].debug = True
mntpun["check_errors"].set_debug_limit(10)

mntitl["check_errors"].debug = True
mntitl["check_errors"].set_debug_limit(10)

mntscr["check_errors"].debug = True
mntscr["check_errors"].set_debug_limit(10)

mntmap["check_errors"].debug = True
mntmap["check_errors"].set_debug_limit(10)

mntall["check_errors"].debug = True
mntall["check_errors"].set_debug_limit(10)

mntext["check_errors"].debug = True
mntext["check_errors"].set_debug_limit(10)

mntdem["check_errors"].debug = True
mntdem["check_errors"].set_debug_limit(10)

mntdsc["check_errors"].debug = True
mntdsc["check_errors"].set_debug_limit(10)

mntdit["check_errors"].debug = True
mntdit["check_errors"].set_debug_limit(10)

mntrec["check_errors"].debug = True
mntrec["check_errors"].set_debug_limit(10)

mntsho["check_errors"].debug = True
mntsho["check_errors"].set_debug_limit(10)

mntcon["check_errors"].debug = True
mntcon["check_errors"].set_debug_limit(10)

mntofm["check_errors"].debug = True
mntofm["check_errors"].set_debug_limit(10)

mntofd["check_errors"].debug = True
mntofd["check_errors"].set_debug_limit(10)

mnt["check_errors"].debug = True
mnt["check_errors"].set_debug_limit(10)


l_tasks = seq.get_tasks_per_types()
for lt in l_tasks:
    for t in lt:
        t.stats = True

print("-----------------SOURCE---------------------------------------------------------------------------------------------")
src["generate"].exec()
srca["generate"].exec()
c_srca["generate"].exec()
mntsrc["check_errors"].exec()

crc["build"].exec()

if (C!=1):
    seg["segment"].exec()
    rcc["build"].exec()
    print("-----------------SEGMENT---------------------------------------------------------------------------------------------")
    c_seg["segment"].exec()
    mntseg["check_errors"].exec()

print("-----------------FILL---------------------------------------------------------------------------------------------")
fill["fill"].exec()
c_fill["fill"].exec()
mntfil["check_errors"].exec()

print("-----------------ENCODE---------------------------------------------------------------------------------------------")
enc["encode"].exec()
c_enc["encode"].exec()
mntenc["check_errors"].exec()


print("-----------------PUNCTURE---------------------------------------------------------------------------------------------")
pun["puncture"].exec()
c_pun["puncture"].exec()
mntpun["check_errors"].exec()

print("-----------------INTERLEAVE---------------------------------------------------------------------------------------------")
itl["interleave"].exec()
c_itl["interleave"].exec()
mntitl["check_errors"].exec()

print("-----------------SCRAMBLE---------------------------------------------------------------------------------------------")
scr["scramble"].exec()
c_scr["scramble"].exec()
mntscr["check_errors"].exec()

print("-----------------MAP---------------------------------------------------------------------------------------------")
mdm["modulate"].exec()
lmap["map"].exec()
c_lmap["map"].exec()
mntmap["check_errors"].exec()


print("-----------------PRECODE---------------------------------------------------------------------------------------------")
prc["precode"].exec()
c_prc["precode"].exec()

print("-----------------ALLOCATE---------------------------------------------------------------------------------------------")
all["allocate"].exec()
c_all["allocate"].exec()
mntall["check_errors"].exec()

print("-----------------OFDMMOD---------------------------------------------------------------------------------------------")
ofdm["modulate"].exec()
c_ofdm["modulate"].exec()
mntofm["check_errors"].exec()

chn["add_noise"].exec()

print("-----------------OFDMDEM---------------------------------------------------------------------------------------------")
ofdm["demodulate"].exec()
c_ofdm["demodulate"].exec()
mntofd["check_errors"].exec()


print("-----------------EXTRACT---------------------------------------------------------------------------------------------")
all["extract"].exec()
c_all["extract"].exec()
mntext["check_errors"].exec()

chn["dec"].exec()

print("-----------------DECODE---------------------------------------------------------------------------------------------")
prc["decode"].exec()
c_prc["decode"].exec()

print("-----------------DEMAP---------------------------------------------------------------------------------------------")
lmap["demap"].exec()
c_lmap["demap"].exec()
mntdem["check_errors"].exec()

print("-----------------DESCRAMBLE---------------------------------------------------------------------------------------------")
mdm["demodulate"].exec()
scr["descrambleLLR"].exec()
c_scr["descrambleLLR"].exec()
mntdsc["check_errors"].exec()

print("-----------------DEINTERLEAVE---------------------------------------------------------------------------------------------")
itl["deinterleaveLLR"].exec()
c_itl["deinterleaveLLR"].exec()
mntdit["check_errors"].exec()

print("-----------------RECOVER---------------------------------------------------------------------------------------------")
pun["recoverLLR"].exec()
c_pun["recoverLLR"].exec()
mntrec["check_errors"].exec()

print("-----------------SHORTEN---------------------------------------------------------------------------------------------")
dec["decode_siho"].exec()
fill["shorten"].exec()
c_fill["shorten"].exec()
mntsho["check_errors"].exec()

if (C!=1):
    rcc["extract"].exec()
    seg["concatenate"].exec()
    print("-----------------CONCATENATE---------------------------------------------------------------------------------------------")

    c_seg["concatenate"].exec()
    mntcon["check_errors"].exec()

crc["extract"].exec()

print("-----------------ERROR---------------------------------------------------------------------------------------------")
mnt["check_errors"].exec()

print(sum(sum(crc["extract::V_K2"][:]-srca["generate ::V_K"][:])))
print(sum(sum(crc["extract::V_K2"][:]-c_srca["generate ::V_K"][:])))
print(K-Kp)
#print(ofdm["modulate :: Y_N"][:,4000:]-c_ofdm["modulate :: Y_N"][:,4000:])
#print(all["extract :: B_N"][:,1000:1050])
#print(c_all["extract :: B_N"][:,1000:1050])

#import galois
#GF = galois.GF(2)
#HH = np.array(H.full(), dtype=np.int32)
#print(HH[0:10,0:10])
#print(HH[0,:].size,HH[:,0].size, K, N)
#print(np.dot(GF(enc["encode :: X_N"][:]),GF(HH)))
#print(np.dot(GF(c_enc["encode :: X_N"][:]),GF(HH)))
#seq.show_stats()

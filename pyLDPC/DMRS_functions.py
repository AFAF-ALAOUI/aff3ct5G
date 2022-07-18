
import numpy as np
import math


def DMRS_TimePosPerSlot(DMRS_length, Mapping_type, freq_hop, TypeAPos, add_pos, sym_duration):
    if (DMRS_length == 1):
        if (freq_hop == 0): # disabled
            if (Mapping_type == 'A'):
                DMRS = [[-1, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos],
                [-1, TypeAPos, TypeAPos, TypeAPos, TypeAPos, [TypeAPos,7], [TypeAPos,7] ,[TypeAPos,9], [TypeAPos,9], [TypeAPos,9], [TypeAPos,11], [TypeAPos,11]],
                [-1, TypeAPos, TypeAPos, TypeAPos, TypeAPos, [TypeAPos,7], [TypeAPos,7] ,[TypeAPos,6,9], [TypeAPos,6,9], [TypeAPos,6,9], [TypeAPos,7,11], [TypeAPos,7,11]],
                [-1, TypeAPos, TypeAPos, TypeAPos, TypeAPos, [TypeAPos,7], [TypeAPos,7] ,[TypeAPos,6,9], [TypeAPos,6,9], [TypeAPos,5,8,11], [TypeAPos,5,8,11], [TypeAPos,5,8,11]]]

            elif (Mapping_type == 'B'):
                DMRS = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, [0,4], [0,4], [0,4], [0,6], [0,6] ,[0,8], [0,8], [0,10], [0,10], [0,10]],
                [0, 0, [0,4], [0,4], [0,4], [0,3,6], [0,3,6] ,[0,4,8], [0,4,8], [0,5,10], [0,5,10], [0,5,10]],
                [0, 0, [0,4], [0,4], [0,4], [0,3,6], [0,3,6] ,[0,3,6,9], [0,3,6,9], [0,3,6,9], [0,3,6,9], [0,3,6,9]]]

        else :    # freq_hop enabled
            if (Mapping_type == 'A'):
                if (TypeAPos == 2):
                    DMRS = [[[-1, TypeAPos, TypeAPos, TypeAPos], [-1, 0, 0, 0]],
                    [[-1, TypeAPos, TypeAPos, [TypeAPos,6]], [-1, 0, [0,4], [0,4]]]]

                elif (TypeAPos == 3):
                    DMRS = [[[-1, TypeAPos, TypeAPos, TypeAPos], [-1, 0, 0, 0]],
                    [[-1, TypeAPos, TypeAPos, TypeAPos], [-1, 0, [0,4], [0,4]]]]


            elif (Mapping_type == 'B'):
                DMRS = DMRS = [[[0, 0, 0, 0], [0, 0, 0, 0]],
                [[0, 0, [0,4], [0,4]], [0, 0, [0,4], [0,4]]]]


    elif(DMRS_length == 2):
        if (Mapping_type == 'A'):
            DMRS = [[-1, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos],
            [-1, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos ,[TypeAPos,8], [TypeAPos,8], [TypeAPos,8], [TypeAPos,10], [TypeAPos,10]]]

        elif (Mapping_type == 'B'):
            DMRS = [[-1, -1, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos, TypeAPos],
            [-1, -1, TypeAPos, TypeAPos, TypeAPos, [TypeAPos,5], [TypeAPos,5] ,[TypeAPos,7], [TypeAPos,7], [TypeAPos,9], [TypeAPos,9], [TypeAPos,9]]]


    ld = 0 if sym_duration < 4 else sym_duration-3
    l = DMRS[add_pos][ld]
    DMRS_list = [l] if (type(l) is int) else l


    return DMRS_list

def DMRS_DL(DMRS_list):
    DMRS_list.extend([i+1 for i in DMRS_list])
    DMRS_list = np.sort(DMRS_list)
    return DMRS_list

def DMRS_TimePos(Nslot,Nofdms, DMRS_length, Mapping_type, freq_hop, TypeAPos, add_pos, sym_duration):
    list = DMRS_TimePosPerSlot(DMRS_length, Mapping_type, freq_hop, TypeAPos, add_pos, sym_duration)
    if (DMRS_length==2):
        list = DMRS_DL(list)
    DMRS_list = [i+k*Nofdms for k in range(Nslot)for i in list]
    return DMRS_list

def DMRS_freqTimePos(DMRS_TPos,Msc):
    return [Msc*i+k for i in DMRS_TPos for k in range(Msc)]

def DMRS_FreqPos(Conf_type, Mrb, Nl):
    k = [0]*6*Mrb if Conf_type == 1 else [0]*4*Mrb
    Index = np.arange(0,12*Mrb)
    if Conf_type == 1:
        delta = 1 if (Nl%4 == 2 or Nl%4 ==3) else 0
        k = Index[delta::2]

    elif Conf_type == 2:
        if (Nl%6 == 4 or Nl%6 ==5):
            delta = 4
        elif (Nl%6 == 2 or Nl%6 ==3):
            delta = 2
        else:
            delta = 0
        k[0::2] = Index[delta::6]
        k[1::2] = Index[delta+1::6]

    else :
        print('Invalid Configuration_type')

    return k


def DMRS_perOFDMS(Conf_type, Mrb):
    return 6*Mrb*(Conf_type==1) + 4*Mrb*(Conf_type == 2)

def LAMBDA_value(Nl, Conf_type):

    if Conf_type == 1:
        lamda = 1 if (Nl%4 == 2 or Nl%4 ==3) else 0

    elif Conf_type == 2:
        if (Nl%6 == 4 or Nl%6 ==5):
            lamda = 2
        elif (Nl%6 == 2 or Nl%6 ==3):
            lamda = 1
        else:
            lamda = 0


    return lamda

def Data_TimePos(DMRS_TPos,Nslot,Nofdms):
    return [i for i in range(Nslot*Nofdms) if i not in DMRS_TPos]

def Data_freqPos(Data_TPos,Msc):
    return [Msc*i+k for i in Data_TPos for k in range(Msc)]

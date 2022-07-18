
import numpy as np
import math


##5
TAB5_1 = [[2,120,0.2344],[2,157,0.3066],[2,193,0.3770],[2,251,0.4902],[2,308,0.6016],[2,379,0.7402],[2,449,0.8770],[2,526,1.0273],[2,602,1.1758],[2,679,1.3262],[4,340,1.3281],[4,378,1.4766],[4,434,1.6953],[4,490,1.9141],[4,553,2.1602],[4,616,2.4063],[4,658,2.5703],[6,438,2.5664],[6,466,2.7305],[6,517,3.0293],[6,567,3.3223],[6,616,3.6094],[6,666,3.9023],[6,719,4.2129],[6,772,4.5234],[6,822,4.8164],[6,873,5.1152],[6,910,5.3320],[6,948,5.5547]]
TAB5_2 = [[2,120,0.2344],[2,193,0.3770],[2,308,0.6016],[2,449,0.8770],[2,602,1.1758],[4,378,1.4766],[4,434,1.6953],[4,490,1.9141],[4,553,2.1602],[4,616,2.4063],[4,658,2.5703],[6,466,2.7305],[6,517,3.0293],[6,567,3.3223],[6,616,3.6094],[6,666,3.9023],[6,719,4.2129],[6,772,4.5234],[6,822,4.8164],[6,873,5.1152],[8,682.5,5.3320],[8,711,5.5547],[8,754,5.8906],[8,797,6.2266],[8,841,6.5703],[8,885,6.9141],[8,916.5,7.1602],[8,948,7.4063]]
TAB5_3 = [[2,30,0.0586],[2,40,0.0781],[2,50,0.0977],[2,64,0.1250],[2,78,0.1523],[2,99,0.1934],[2,120,0.2344],[2,157,0.3066],[2,193,0.3770],[2,251,0.4902],[2,308,0.6016],[2,379,0.7402],[2,449,0.8770],[2,526,1.0273],[2,602,1.1758],[4,340,1.3281],[4,378,1.4766],[4,434,1.6953],[4,490,1.9141],[4,553,2.1602],[4,616,2.4063],[6,438,2.5664],[6,466,2.7305],[6,517,3.0293],[6,567,3.3223],[6,616,3.6094],[6,666,3.9023],[6,719,4.2129],[6,772,4.5234]]
TAB5_4 = [[2,120,0.2344],[2,193,0.3770],[2,449,0.8770],[4,378,1.4766],[4,490,1.9141],[6,466,2.7305],[6,517,3.0293],[6,567,3.3223],[6,616,3.6094],[6,666,3.9023],[6,719,4.2129],[6,772,4.5234],[6,822,4.8164],[6,873,5.1152],[8,682.5,5.3320],[8,711,5.5547],[8,754,5.8906],[8,797,6.2266],[8,841,6.5703],[8,885,6.9141],[8,916.5,7.1602],[8,948,7.4063],[10,805.5,7.8662],[10,853,8.3301],[10,900.5,8.7939],[10,948,9.2578]]


##6
TAB6_1  = [[2,120,0.2344],[2,157,0.3066],[2,193,0.3770],[2,251,0.4902],[2,308,0.6016],[2,379,0.7402],[2,449,0.8770],[2,526,1.0273],[2,602,1.1758],[2,679,1.3262],[4,340,1.3281],[4,378,1.4766],[4,434,1.6953],[4,490,1.9141],[4,553,2.1602],[4,616,2.4063],[4,658,2.5703],[6,466,2.7305],[6,517,3.0293],[6,567,3.3223],[6,616,3.6094],[6,666,3.9023],[6,719,4.2129],[6,772,4.5234],[6,822,4.8164],[6,873,5.1152],[6,910,5.3320],[6,948,5.5547]]
TAB6_11 = [[1,240,0.2344],[1,314,0.3066],[2,193,0.3770],[2,251,0.4902],[2,308,0.6016],[2,379,0.7402],[2,449,0.8770],[2,526,1.0273],[2,602,1.1758],[2,679,1.3262],[4,340,1.3281],[4,378,1.4766],[4,434,1.6953],[4,490,1.9141],[4,553,2.1602],[4,616,2.4063],[4,658,2.5703],[6,466,2.7305],[6,517,3.0293],[6,567,3.3223],[6,616,3.6094],[6,666,3.9023],[6,719,4.2129],[6,772,4.5234],[6,822,4.8164],[6,873,5.1152],[6,910,5.3320],[6,948,5.5547]]
TAB6_2  = [[2,30,0.0586],[2,40,0.0781],[2,50,0.0977],[2,64,0.1250],[2,78,0.1523],[2,99,0.1934],[2,120,0.2344],[2,157,0.3066],[2,193,0.3770],[2,251,0.4902],[2,308,0.6016],[2,379,0.7402],[2,449,0.8770],[2,526,1.0273],[2,602,1.1758],[2,679,1.3262],[4,378,1.4766],[4,434,1.6953],[4,490,1.9141],[4,553,2.1602],[4,616,2.4063],[4,658,2.5703],[4,699,2.7305],[4,772,3.0156],[6,567,3.3223],[6,616,3.6094],[6,666,3.9023],[6,772,4.5234]]
TAB6_22 = [[1,60,0.0586],[1,80,0.0781],[1,100,0.0977],[1,128,0.1250],[1,156,0.1523],[1,198,0.1934],[2,120,0.2344],[2,157,0.3066],[2,193,0.3770],[2,251,0.4902],[2,308,0.6016],[2,379,0.7402],[2,449,0.8770],[2,526,1.0273],[2,602,1.1758],[2,679,1.3262],[4,378,1.4766],[4,434,1.6953],[4,490,1.9141],[4,553,2.1602],[4,616,2.4063],[4,658,2.5703],[4,699,2.7305],[4,772,3.0156],[6,567,3.3223],[6,616,3.6094],[6,666,3.9023],[6,772,4.5234]]



TBS = [24,32,40,48,56,64,72,80,88,96,104,112,120,128,136,144,152,160,168,176,184,192,208,224,240,256,272,288,304,320,336,352,352,368,384,408,432,456,480,504,528,552,576,608,640,672,704,736,768,808,848,888,928,984,1032,1064,1128,1160,1192,1224,1256,1288,1320,1416,1480,1544,1608,1672,1736,1800,1864,1928,2024,2088,2152,2216,2280,2408,2472,2536,2600,2664,2728,2792,2856,2976,3104,3240,3368,3496,3624,3752,3824]

def transportBlocSize(N_sh_symb, N_DMRS_RB, N_Oh_RB, Mrb, R, Qm, Nl):

    Np_RE = 12 * N_sh_symb - N_DMRS_RB - N_Oh_RB
    N_RE  = min(156, Np_RE)* Mrb
    Ninfo = N_RE *R*Qm*Nl
    if (Ninfo <= 3824):
        n = max(3,math.floor(math.log2(Ninfo))-6)
        Nif = max(24, 2**n* math.floor(Ninfo/2**n))
        tbs = [i for i in TBS if (i >= Nif)][0]
    else:
        n = math.floor(math.log2(Ninfo-24))-5
        Nif  = max(3840,2**n*round((Ninfo-24)/(2**n)))
        if (R <= 1/4):
            C = math.ceil((Nif+24)/3816)
            tbs = 8*C * math.ceil((Nif+24)/(8*C)) -24
        else:
            C = math.ceil((Nif+24)/8424)
            tbs = 8*C * math.ceil((Nif+24)/(8*C))-24  if (Nif > 8424) else 8 * math.ceil((Nif+24)/8)-24

    return tbs
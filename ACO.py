import math
import random
from matplotlib import pyplot as plt
import time



def f(rjesenje, tezinska_matrica):
    put = 0
    put += tezinska_matrica[rjesenje[0] - 1][rjesenje[1] - 1]
    for i in range(1, len(rjesenje) - 1):
        put += tezinska_matrica[rjesenje[i] - 1][rjesenje[i + 1] - 1]
    put += tezinska_matrica[rjesenje[len(rjesenje) - 1] - 1][rjesenje[0] - 1]
    return put

def pocetno_rjesenje(tezinska_matrica):
    i = 0
    brojac = 0
    posjeceni = [0]
    while brojac < len(tezinska_matrica) - 1:
        brojac += 1
        bez_nula = [x for x in tezinska_matrica[i]]
        for k in range(len(bez_nula)):
            if k in posjeceni:
                bez_nula[k] = 0
        bez_nula = [x for x in bez_nula if x > 0]
        minimalni = min(bez_nula)
        for j in range(len(tezinska_matrica)):
            if tezinska_matrica[i][j] == minimalni:
                pamti_j = j
                posjeceni.append(pamti_j)
                break
        i = pamti_j
    for m in range(len(posjeceni)):
        posjeceni[m] += 1
    return posjeceni


def greedy(tezine,pocetnaTacka):    
    konacnaLista=[pocetnaTacka]
    oznacenePozicije=[pocetnaTacka]
    i=pocetnaTacka
    for brojac in range(1,len(tezine)):
        trenutneTezine=[x for x in tezine[i]]
        for j in range(len(trenutneTezine)):
            if(j in oznacenePozicije):
                trenutneTezine[j]=0
        trenutneTezine=[x for x in trenutneTezine if x != 0]
        if(len(trenutneTezine)==0):
            break
        minimum=min(trenutneTezine)
        trenutneTezine=[x for x in tezine[i]]
        indeksMinimuma=trenutneTezine.index(minimum)
        konacnaLista.append(indeksMinimuma)
        oznacenePozicije.append(indeksMinimuma)
        i=indeksMinimuma
    return konacnaLista
            
                    
def funkcijaCilja(cvorovi,tezine):
    pocetni=cvorovi[0]
    sljedeci=cvorovi[1]
    suma=0
    for i in range(1,len(cvorovi)):
        sljedeci=cvorovi[i]
        suma=suma+tezine[pocetni][sljedeci]
        pocetni=sljedeci
    suma=suma+tezine[pocetni][cvorovi[0]]
    return suma


def KonstruirajRjesenje(alfa,beta,tau,tezinskaMatrica):
    i=random.choice(range(len(tezinskaMatrica)))
    rjesenje=[i]
    for brojac in range(len(tezinskaMatrica)-1):
        dozvoljenaOkolina=[]
        for broj in range(0,len(tezinskaMatrica)):
            dozvoljenaOkolina.append(broj)
        dozvoljenaOkolina=[x for x in dozvoljenaOkolina if x not in rjesenje]
        vjerovatnocaGrane=[]
        for broj in range(0,len(tezinskaMatrica)):
            vjerovatnocaGrane.append(0)
        nazivnik=0
        for l in dozvoljenaOkolina:
            nazivnik+=pow(tau[i][l],alfa)*pow((1/tezinskaMatrica[i][l]),beta)
        for j in dozvoljenaOkolina:
            eta=1/tezinskaMatrica[i][j]
            brojnik=pow(tau[i][j],alfa)*pow(eta,beta)
            if(nazivnik!=0):
                vjerovatnocaGrane[j]=brojnik/nazivnik
        maksimum=max(vjerovatnocaGrane)
        indeksMaksimuma=vjerovatnocaGrane.index(maksimum)
        i=indeksMaksimuma
        rjesenje.append(i)
    return rjesenje

def IsparavanjeFeromonskogTraga(tau,ro):
    for i in range(len(tau)):
        for j in range(len(tau[i])):
            tau[i][j]*=(1-ro)
    return tau

def plot(cvorovi,rjesenje,line_width=1, point_radius=math.sqrt(2.0), annotation_size=8, dpi=120):
        x = [cvorovi[i][0] for i in rjesenje]
        x.append(x[0])
        y = [cvorovi[i][1] for i in rjesenje]
        y.append(y[0])
        plt.plot(x, y, linewidth=line_width)
        plt.scatter(x, y, s=math.pi * (point_radius ** 2.0))
        plt.title("Nadjeno rjesenje GA")
        for i in rjesenje:
            plt.annotate(i, cvorovi[i], size=annotation_size)
        plt.show()

def elitistickiACO(f,x0,tezinskaMatrica,brojMrava,brojIteracija,alfa,beta,ro,e):
    xZvijezda=[]
    vZvijezda=float("inf")
    tau=[]
    v0=f(x0,tezinskaMatrica)
    pocetnoTau=(e+brojMrava)/(ro*v0)
    for i in range(len(tezinskaMatrica)):
        lista=[]
        for j in range(len(tezinskaMatrica[i])):
            if(i!=j):
                lista.append(pocetnoTau)
            else:
                lista.append(0)
        tau.append(lista)
    
    while(brojIteracija>0):
        omegaPrim=[]
        omegaV=[]
        for k in range(brojMrava):
            xPrim=KonstruirajRjesenje(alfa,beta,tau,tezinskaMatrica)
            vPrim=f(xPrim,tezinskaMatrica)
            if(vPrim<vZvijezda):
                xZvijezda=xPrim
                vZvijezda=vPrim
            omegaPrim.append(xPrim)
            omegaV.append(f(xPrim,tezinskaMatrica))
        tau=[x for x in IsparavanjeFeromonskogTraga(tau,ro)]
        for i in range(len(omegaPrim)):
            xP=omegaPrim[i]
            for j in range(len(xP)-1):
                tau[xP[j]][xP[j+1]]+=1.0/omegaV[i]
                tau[xP[j+1]][xP[j]]+=1.0/omegaV[i]
            tau[xP[j]][xP[0]]+=1.0/omegaV[i]
            tau[xP[0]][xP[j]]+=1.0/omegaV[i]
        

        for j in range(len(xZvijezda)-1):
            tau[xZvijezda[j]][xZvijezda[j+1]]+=e/vZvijezda
            tau[xZvijezda[j+1]][xZvijezda[j]]+=e/vZvijezda
        tau[xZvijezda[j]][xZvijezda[0]]+=e/vZvijezda
        tau[xZvijezda[0]][xZvijezda[j]]+=e/vZvijezda
        brojIteracija-=1
    return (xZvijezda,vZvijezda)



def ACO(f,x0,tezinskaMatrica,brojMrava,brojIteracija,alfa,beta,ro):
    xZvijezda=[]
    vZvijezda=float("inf")
    tau=[]
    v0=f(x0,tezinskaMatrica)
    pocetnoTau=brojMrava/v0
    for i in range(len(tezinskaMatrica)):
        lista=[]
        for j in range(len(tezinskaMatrica[i])):
            if(i!=j):
                lista.append(pocetnoTau)
            else:
                lista.append(0)
        tau.append(lista)
    
    while(brojIteracija>0):
        omegaPrim=[]
        omegaV=[]
        for k in range(brojMrava):
            xPrim=KonstruirajRjesenje(alfa,beta,tau,tezinskaMatrica)
            vPrim=f(xPrim,tezinskaMatrica)
            if(vPrim<=vZvijezda):
                xZvijezda=xPrim
                vZvijezda=vPrim
            omegaPrim.append(xPrim)
            omegaV.append(f(xPrim,tezinskaMatrica))
        tau=[x for x in IsparavanjeFeromonskogTraga(tau,ro)]
        for i in range(len(omegaPrim)):
            xP=omegaPrim[i]
            for j in range(len(xP)-1):
                tau[xP[j]][xP[j+1]]+=1.0/omegaV[i]
                tau[xP[j+1]][xP[j]]+=1.0/omegaV[i]
            tau[xP[j]][xP[0]]+=1.0/omegaV[i]
            tau[xP[0]][xP[j]]+=1.0/omegaV[i]
        brojIteracija-=1
    return (xZvijezda,vZvijezda)



def konstruisi_rjesenje(tezinska_matrica, matrica_feromonski_trag, alfa, beta):
    brojac = 0
    posjeceni = [random.choice(range(len(tezinska_matrica)))]
    l = posjeceni[0] 
    while brojac < len(tezinska_matrica) - 1:
        brojac += 1
        bez_nula = [x for x in tezinska_matrica[l]]
        for k in range(len(bez_nula)):
            if k in posjeceni:
                bez_nula[k] = 0
        suma = 0
        vjerovatnoce = [0] * len(bez_nula)
        for t in range(len(bez_nula)):
            if bez_nula[t] != 0:
                ni = 1/tezinska_matrica[l][t]
                suma += (pow(matrica_feromonski_trag[l][t], alfa) * pow(ni, beta))
        for r in range(len(bez_nula)):
            if bez_nula[r] != 0:
                ni = 1/tezinska_matrica[l][r]
                p = (pow(matrica_feromonski_trag[l][r], alfa) * pow(ni, beta))/suma
                vjerovatnoce[r] = p
        vjerovatnoce_bez_nula = [x for x in vjerovatnoce if x > 0]       
        maksimalna_p = max(vjerovatnoce_bez_nula)
        for j in range(len(vjerovatnoce)):
            if vjerovatnoce[j] == maksimalna_p and j not in posjeceni:
                pamti_j = j
                posjeceni.append(pamti_j)
                break
        l = pamti_j
    for m in range(len(posjeceni)):
        posjeceni[m] += 1
    return posjeceni


def isparavanje_feromonskog_traga_MMAS(matrica_feromonski_trag, ro, Cbs):
    tau_max = 1/(ro * Cbs)
    tau_min = tau_max * 0.001
    for i in range(len(matrica_feromonski_trag)):
        for j in range(len(matrica_feromonski_trag)):
            if i != j:
                matrica_feromonski_trag[i][j] *= (1 - ro) 
                if matrica_feromonski_trag[i][j] > tau_max:
                    matrica_feromonski_trag[i][j] = tau_max
                if matrica_feromonski_trag[i][j] < tau_min:
                    matrica_feromonski_trag[i][j] = tau_min
    return matrica_feromonski_trag

def azuriraj_feromonski_trag_MMAS(najbolje_rjesenje, tezinska_matrica, matrica_feromonski_trag, Cbs, ro):
    Ck = f(najbolje_rjesenje, tezinska_matrica)
    delta_tau = 1/Ck
    tau_max = 1/(ro * Cbs)
    tau_min = tau_max * 0.001
    for j in range(len(najbolje_rjesenje) - 1):
        matrica_feromonski_trag[najbolje_rjesenje[j] - 1][najbolje_rjesenje[j + 1] - 1] += delta_tau
        matrica_feromonski_trag[najbolje_rjesenje[j + 1] - 1][najbolje_rjesenje[j] - 1] += delta_tau
    matrica_feromonski_trag[najbolje_rjesenje[len(najbolje_rjesenje) - 1] - 1][najbolje_rjesenje[0] - 1] += delta_tau
    matrica_feromonski_trag[najbolje_rjesenje[0] - 1][najbolje_rjesenje[len(najbolje_rjesenje) - 1] - 1] += delta_tau
    return matrica_feromonski_trag

def reinicijaliziraj_MMAS(tezinska_matrica, matrica_feromonski_trag, Cbs, ro):
    tau_max = 1/(ro * Cbs)
    for i in range(len(matrica_feromonski_trag)):
        for j in range(len(matrica_feromonski_trag)):
            if i != j:
                matrica_feromonski_trag[i][j] = tau_max
                matrica_feromonski_trag[j][i] = tau_max
            else:
                matrica_feromonski_trag[i][j] = 0
    return matrica_feromonski_trag
        
    
def MMAS(alfa, beta, ro, tezinska_matrica, m, N, M):
    x_zvijezda = []
    v_zvijezda = float("inf")
    broj_iteracija = 0
    reincijaliziraj = 0
    
    pocetno = pocetno_rjesenje(tezinska_matrica)
    Cnn = f(pocetno, tezinska_matrica)
    x_min = pocetno
    v_min = Cnn
    tau0 = 1/(ro * Cnn)
    feromonski_trag = ([0] * len(tezinska_matrica))
    matrica_feromonski_trag = []
    
    #inicijalizacija feromonskog traga
    for i in range(len(feromonski_trag)):
        feromonski_trag = ([0] * len(tezinska_matrica))
        for j in range(len(feromonski_trag)):
            if i != j:
                feromonski_trag[j] = tau0
        matrica_feromonski_trag.append(feromonski_trag)
        
    while 1:
        broj_iteracija += 1
        omega = []
        putanje = []
        for i in range(m):
            
            #konstruisi rjesenje
            posjeceni = konstruisi_rjesenje(tezinska_matrica, matrica_feromonski_trag, alfa, beta)
            
            x_prim = posjeceni
            v_prim = f(x_prim, tezinska_matrica)

            if v_prim < v_zvijezda:
                v_zvijezda = v_prim
                x_zvijezda = x_prim
            omega.append(x_prim)
            putanje.append(v_prim)
        
        if v_zvijezda == v_min:
            reincijaliziraj += 1
        
        if v_zvijezda < v_min:
            v_min = v_zvijezda
            x_min = x_zvijezda

        #isparavanje feromonskog traga
        matrica_feromonski_trag = isparavanje_feromonskog_traga_MMAS(matrica_feromonski_trag, ro, v_min)

        #azuriraj feromonski trag
        random_broj = random.choice(range(0, 100))
        if random_broj % 2 == 0:
            najbolje_rjesenje = x_zvijezda
        else:
            minimalni = min(putanje)
            for h in range(len(omega)):
                if putanje[h] == minimalni:
                    najbolje_rjesenje = omega[h]
        matrica_feromonski_trag = azuriraj_feromonski_trag_MMAS(najbolje_rjesenje, tezinska_matrica, matrica_feromonski_trag, v_min, ro)
        
        if reincijaliziraj == M:
            matrica_feromonski_trag = reinicijaliziraj_MMAS(tezinska_matrica, matrica_feromonski_trag, v_min, ro)
            reincijaliziraj = 0

        if broj_iteracija == N:
            break
    return x_min, v_min 


if __name__=="__main__":  
    
    W1 = [[0,2,2,2,7,5,2],
      [2,0,4,7,9,1,3],
      [2,4,0,3,6,6,5],
      [2,7,3,0,4,9,6],
      [7,9,6,4,0,4,9],
      [5,1,6,9,4,0,2],
      [2,3,5,6,9,2,0]]
    #rjesenje W1: 19
    
    
    
    
    
    W2 = [[0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
        [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
        [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
        [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
        [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
        [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
        [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
        [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
        [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
        [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
        [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
        [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
        [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0]]
    #rjesenje za W2: 7293
    
    W3 = [[0, 633, 257,  91, 412, 150 , 80, 134, 259, 505 ,353, 324 , 70, 211, 268, 246, 121],
        [633,   0, 390, 661, 227, 488, 572, 530, 555, 289, 282, 638, 567, 466, 420, 745, 518],
        [257, 390,   0, 228, 169, 112, 196, 154, 372, 262, 110, 437, 191,  74,  53, 472, 142],
        [91, 661, 228,   0, 383, 120 , 77, 105, 175, 476, 324, 240,  27, 182, 239, 237,  84],
        [412, 227, 169, 383, 0, 267, 351, 309, 338, 196,  61, 421, 346, 243 ,199, 528, 297],
        [150, 488, 112, 120, 267,   0,  63,  34, 264, 360, 208, 329,  83, 105, 123, 364,  35],
        [80, 572, 196,  77, 351,  63 ,  0 , 29, 232, 444, 292, 297 , 47, 150, 207, 332,  29],
        [134, 530, 154, 105, 309,  34,  29,   0, 249, 402, 250, 314,  68, 108, 165, 349,  36],
        [259, 555, 372, 175, 338, 264, 232, 249,   0, 495, 352,  95, 189, 326, 383, 202, 236],
        [505, 289, 262, 476, 196, 360, 444, 402, 495,   0, 154, 578, 439, 336, 240, 685, 390],
        [353, 282, 110, 324,  61, 208, 292, 250, 352, 154,   0, 435, 287, 184, 140, 542, 238],
        [324, 638, 437, 240, 421, 329, 297, 314,  95, 578, 435,   0, 254, 391, 448, 157, 301],
        [70, 567, 191,  27, 346 , 83 , 47 , 68, 189, 439, 287, 254,   0, 145, 202, 289,  55],
        [211, 466,  74, 182, 243, 105, 150, 108, 326, 336, 184, 391, 145,   0,  57, 426,  96],
        [268, 420,  53, 239, 199, 123, 207, 165, 383, 240, 140, 448, 202,  57,   0, 483, 153],
        [246, 745, 472, 237, 528, 364, 332, 349, 202, 685, 542, 157, 289, 426, 483,   0, 336],
        [121, 518, 142,  84, 297,  35,  29,  36, 236, 390, 238, 301,  55 , 96, 153, 336,   0]]
    #rjesenje W3: 2085
    
    W4=[[0,  83,  93, 129, 133, 139, 151, 169, 135, 114, 110,  98,  99,  95, 81, 152, 159, 181, 172, 185, 147, 157, 185, 220, 127, 181],
        [83,  0, 40,  53,  62,  64,  91, 116,  93,  84,  95,  98,  89,  68,  67, 127, 156, 175, 152, 165, 160, 180, 223, 268, 179, 197],
        [93,  40,   0,  42,  42,  49,  59,  81,  54,  44,  58,  64,  54,  31,  36,  86, 117, 135, 112, 125, 124, 147, 193, 241, 157, 161],
        [129,  53,  42,   0,  11,  11,  46,  72, 65,  70,  88, 100,  89,  66,  76, 102, 142, 156, 127, 139, 155, 180, 228, 278, 197, 190],
        [133,  62,  42,  11,   0,   9,  35,  61, 55,  62, 82,  95,  84,  62,  74,  93, 133, 146, 117, 128, 148, 173, 222, 272, 194, 182],
        [139,  64,  49,  11,   9,   0,  39,  65,  63,  71,  90, 103,  92,  71,  82, 100, 141, 153, 124, 135, 156, 181, 230, 280, 202, 190],
        [151, 91,  59, 46,  35,  39,   0,  26,  34,  52,  71,  88,  77,  63,  78,  66, 110, 119,  88,  98, 130, 156, 206, 257, 188, 160],
        [169, 116,  81,  72,  61,  65,  26,   0,  37,  59,  75,  92,  83,  76,  91,  54,  98, 103,  70,  78, 122, 148, 198, 250, 188, 148],
        [135,  93,  54,  65,  55,  63,  34, 37,   0, 22,  39,  56,  47,  40,  55,  37,  78,  91,  62,  74,  96, 122, 172, 223, 155, 128],
        [114,  84,  44,  70,  62,  71,  52,  59,  22,   0,  20,  36,  26,  20,  34,  43,  74,  91,  68,  82,  86, 111, 160, 210, 136, 121],
        [110,  95,  58, 88,  82,  90, 71,  75,  39,  20,   0,  18, 11,  27,  32,  42,  61,  80,  64,  77,  68,  92, 140, 190, 116, 103],
        [98,  98,  64, 100,  95, 103, 88,  92,  56,  36,  18,   0,  11,  34,  31,  56,  63,  85,  75,  87,  62,  83, 129, 178, 100,  99],
        [99,  89,  54,  89,  84,  92,  77,  83,  47,  26,  11,  11,   0,  23,  24,  53,  68,  89,  74,  87,  71,  93, 140, 189, 111, 107],
        [95, 68, 31,  66,  62,  71,  63,  76,  40,  20,  27,  34,  23,   0,  15,  62,  87, 106,  87, 100,  93, 116, 163, 212, 132, 130],
        [81,  67,  36,  76,  74,  82,  78,  91,  55,  34,  32,  31,  24,  15,   0,  73,  92, 112,  96, 109,  93, 113, 158, 205, 122, 130],
        [152, 127,  86, 102,  93, 100,  66,  54,  37,  43,  42,  56,  53,  62,  73,   0,  44,  54,  26,  39,  68,  94, 144, 196, 139,  95],
        [159, 156, 117,142, 133, 141, 110, 98,  78,  74,  61,  63,  68,  87,  92,  44,   0,  22, 34,  38,  30,  53, 102, 154, 109,  51],
        [181, 175, 135, 156, 146, 153, 119, 103,  91,  91,  80,  85,  89, 106, 112,  54,  22,   0,  33,  29,  46,  64, 107, 157, 125,  51],
        [172, 152, 112, 127, 117, 124,  88,  70,  62,  68,  64,  75,  74,  87,  96,  26,  34,  33,   0,  13,  63,  87, 135, 186, 141,  81],
        [185, 165, 125, 139, 128, 135,  98,  78,  74,  82,  77,  87,  87, 100, 109,  39,  38,  29,  13,   0,  68,  90, 136, 186, 148,  79],
        [147, 160, 124, 155, 148, 156, 130, 122,  96,  86,  68,  62,  71,  93,  93,  68, 30,  46,  63, 68,  0,  26,  77, 128,  80,  37],
        [157, 180, 147, 180, 173, 181, 156, 148, 122, 111,  92,  83,  93, 116, 113,  94,  53,  64,  87,  90,  26,   0,  50, 102,  65,  27],
        [185, 223, 193, 228, 222, 230, 206, 198, 172, 160, 140, 129, 140, 163, 158, 144, 102, 107, 135, 136,  77,  50,   0, 51,  64,  58],
        [220, 268, 241, 278, 272, 280, 257, 250, 223, 210, 190, 178, 189, 212, 205, 196, 154, 157, 186, 186, 128, 102,  51,   0,  93, 107],
        [127, 179, 157, 197, 194, 202, 188, 188, 155, 136, 116, 100, 111, 132, 122, 139, 109, 125, 141, 148, 80,  65,  64,  93,   0,  90],
        [181, 197, 161, 190, 182, 190, 160, 148, 128, 121, 103,  99, 107, 130, 130,  95,  51,  51,  81,  79, 37,  27,  58, 107,  90,   0]]
    #rjesenje W4: 937
    
    W5 = [[0, 107, 241, 190, 124 , 80, 316,  76, 152, 157, 283, 133, 113, 297, 228, 129, 348, 276, 188, 150,  65, 341, 184,  67, 221, 169, 108,  45, 167],
    [107,   0, 148, 137,  88, 127, 336, 183, 134,  95, 254, 180, 101, 234, 175, 176, 265, 199, 182,  67,  42, 278, 271, 146, 251, 105, 191, 139,  79],
    [241, 148,   0, 374, 171, 259, 509, 317, 217, 232, 491, 312, 280, 391, 412, 349, 422, 356, 355, 204, 182, 435, 417, 292, 424, 116, 337, 273,  77],
    [190, 137, 374,   0, 202, 234, 222, 192, 248,  42, 117, 287,  79, 107,  38, 121, 152,  86,  68,  70, 137, 151, 239, 135, 137, 242, 165, 228, 205],
    [124,  88, 171, 202,   0,  61, 392, 202,  46, 160, 319, 112, 163, 322, 240, 232, 314, 287, 238, 155,  65, 366, 300, 175, 307,  57, 220, 121,  97],
    [ 80, 127, 259, 234,  61,   0, 386, 141,  72, 167, 351,  55, 157, 331, 272, 226, 362, 296, 232, 164,  85, 375, 249, 147, 301, 118, 188,  60, 185],
    [316, 336, 509, 222, 392, 386,   0, 233, 438, 254, 202, 439, 235, 254, 210, 187, 313, 266, 154, 282, 321, 298, 168, 249,  95, 437, 190, 314, 435],
    [ 76, 183, 317, 192, 202, 141, 233,   0, 213, 188, 272, 193, 131, 302, 233,  98, 344, 289, 177, 216, 141, 346, 108,  57, 190, 245,  43,  81, 243],
    [152, 134, 217, 248,  46,  72, 438, 213,   0, 206, 365,  89, 209, 368, 286, 278, 360, 333, 284, 201, 111, 412, 321, 221, 353,  72, 266, 132, 111],
    [157,  95, 232,  42, 160, 167, 254, 188, 206,   0, 159, 220,  57, 149,  80, 132, 193, 127, 100,  28,  95, 193, 241, 131, 169, 200, 161, 189, 163],
    [283, 254, 491, 117, 319, 351, 202, 272, 365, 159,   0, 404, 176, 106,  79, 161, 165, 141,  95, 187, 254, 103, 279, 215, 117, 359, 216, 308, 322],
    [133, 180, 312, 287, 112,  55, 439, 193,  89, 220, 404,   0, 210, 384, 325, 279, 415, 349, 285, 217, 138, 428, 310, 200, 354, 169, 241, 112, 238],
    [113, 101, 280,  79, 163, 157, 235, 131, 209,  57, 176, 210,   0, 186, 117,  75, 231, 165,  81,  85,  92, 230, 184,  74, 150, 208, 104, 158, 206],
    [297, 234, 391, 107, 322, 331, 254, 302, 368, 149, 106, 384, 186,   0,  69, 191,  59,  35, 125, 167, 255,  44, 309, 245, 169, 327, 246, 335, 288],
    [228, 175, 412,  38, 240, 272, 210, 233, 286,  80,  79, 325, 117,  69,   0, 122, 122,  56,  56, 108, 175, 113, 240, 176, 125, 280, 177, 266, 243],
    [129, 176, 349, 121, 232, 226, 187,  98, 278, 132, 161, 279,  75, 191, 122,   0, 244, 178,  66, 160, 161, 235, 118,  62,  92, 277,  55, 155, 275],
    [348, 265, 422, 152, 314, 362, 313, 344, 360, 193, 165, 415, 231,  59, 122, 244,   0,  66, 178, 198, 286,  77, 362, 287, 228, 358, 299, 380, 319],
    [276, 199, 356,  86, 287, 296, 266, 289, 333, 127, 141, 349, 165,  35,  56, 178,  66,   0, 112, 132, 220,  79, 296, 232, 181, 292, 233, 314, 253],
    [188, 182, 355,  68, 238, 232, 154, 177, 284, 100,  95, 285,  81, 125,  56,  66, 178, 112,   0, 128, 167, 169, 179, 120,  69, 283, 121, 213, 281],
    [150,  67, 204,  70, 155, 164, 282, 216, 201,  28, 187, 217,  85, 167, 108, 160, 198, 132, 128,   0,  88, 211, 269, 159, 197, 172, 189, 182, 135],
    [ 65,  42, 182, 137,  65,  85, 321, 141, 111,  95, 254, 138,  92, 255, 175, 161, 286, 220, 167,  88,   0, 299, 229, 104, 236, 110, 149,  97, 108],
    [341, 278, 435, 151, 366, 375, 298, 346, 412, 193, 103, 428, 230,  44, 113, 235,  77,  79, 169, 211, 299,   0, 353, 289, 213, 371, 290, 379, 332],
    [184, 271, 417, 239, 300, 249, 168, 108, 321, 241, 279, 310, 184, 309, 240, 118, 362, 296, 179, 269, 229, 353,   0, 121, 162, 345,  80, 189, 342],
    [ 67, 146, 292, 135, 175, 147, 249,  57, 221, 131, 215, 200,  74, 245, 176,  62, 287, 232, 120, 159, 104, 289, 121,   0, 154, 220,  41,  93, 218],
    [221, 251, 424, 137, 307, 301,  95, 190, 353, 169, 117, 354, 150, 169, 125,  92, 228, 181,  69, 197, 236, 213, 162, 154,   0, 352, 147, 247, 350],
    [169, 105, 116, 242,  57, 118, 437, 245,  72, 200, 359, 169, 208, 327, 280, 277, 358, 292, 283, 172, 110, 371, 345, 220, 352,   0, 265, 178,  39],
    [108, 191, 337, 165, 220, 188, 190,  43, 266, 161, 216, 241, 104, 246, 177,  55, 299, 233, 121, 189, 149, 290,  80,  41, 147, 265,   0, 124, 263],
    [ 45, 139, 273, 228, 121,  60, 314,  81, 132, 189, 308, 112, 158, 335, 266, 155, 380, 314, 213, 182,  97, 379, 189,  93, 247, 178, 124,   0, 199],
    [167 , 79 , 77 ,205 , 97 ,185 ,435 ,243 ,111 ,163 ,322 ,238 ,206 ,288 ,243 ,275 ,319 ,253 ,281 ,135 ,108 ,332 ,342 ,218 ,350 , 39 ,263 ,199 ,  0]]
    #rjesenje W5: 2020
    
   
    #MATRICA W1
    x0=greedy(W1,0)
    #obicni ACO
    #100/5
    vrijeme=0
    ACO10=[]
    for i in range(10):
        start=time.time()
        ACO10.append(ACO(funkcijaCilja,x0,W1,5,100,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo rjesenje 100/5 je: ",ACO10)
    print("Prvo rjesenje 100/5 vrijeme je: ",vrijeme/10)
    
    #1000/5
    vrijeme=0
    ACO11=[]
    for i in range(10):
        start=time.time()
        ACO11.append(ACO(funkcijaCilja,x0,W1,5,1000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo rjesenje 1000/5 je: ",ACO11)
    print("Prvo rjesenje 1000/5 vrijeme je: ",vrijeme/10)
    
    #2000/5
    vrijeme=0
    ACO12=[]
    for i in range(10):
        start=time.time()
        ACO12.append(ACO(funkcijaCilja,x0,W1,5,2000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo rjesenje 2000/5 je: ",ACO12)
    print("Prvo rjesenje 2000/5 vrijeme je: ",vrijeme/10)
    
    #100/7
    vrijeme=0
    ACO13=[]
    for i in range(10):
        start=time.time()
        ACO13.append(ACO(funkcijaCilja,x0,W1,7,100,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo rjesenje 100/7 je: ",ACO13)
    print("\rvo rjesenje 100/7 vrijeme je: ",vrijeme/10)
    
    
    #1000/7
    vrijeme=0
    ACO14=[]
    for i in range(10):
        start=time.time()
        ACO14.append(ACO(funkcijaCilja,x0,W1,7,1000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo rjesenje 1000/7 je: ",ACO14)
    print("Prvo rjesenje 1000/7 vrijeme je: ",vrijeme/10)
    
    
    #2000/7
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W1,7,2000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo rjesenje 2000/7 je: ",ACO15)
    print("Prvo rjesenje 2000/7 vrijeme je: ",vrijeme/10)
    
    
    
    
    
    
    #elitisticki ACO
    #100/5
    vrijeme=0
    ACO10=[]
    for i in range(10):
        start=time.time()
        ACO10.append(elitistickiACO(funkcijaCilja,x0,W1,5,100,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo elitisticki rjesenje 100/5 je: ",ACO10)
    print("Prvo elitisticki rjesenje 100/5 vrijeme je: ",vrijeme/10)
    
    #1000/5
    vrijeme=0
    ACO11=[]
    for i in range(10):
        start=time.time()
        ACO11.append(elitistickiACO(funkcijaCilja,x0,W1,5,1000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo elitisticki rjesenje 1000/5 je: ",ACO11)
    print("Prvo elitisticki rjesenje 1000/5 vrijeme je: ",vrijeme/10)
    
    #2000/5
    vrijeme=0
    ACO12=[]
    for i in range(10):
        start=time.time()
        ACO12.append(elitistickiACO(funkcijaCilja,x0,W1,5,2000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo elitisticki rjesenje 2000/5 je: ",ACO12)
    print("Prvo elitisticki rjesenje 2000/5 vrijeme je: ",vrijeme/10)
    
    #100/7
    vrijeme=0
    ACO13=[]
    for i in range(10):
        start=time.time()
        ACO13.append(elitistickiACO(funkcijaCilja,x0,W1,7,100,1,3,0.5,7))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo elitisticki rjesenje 100/7 je: ",ACO13)
    print("\rvo elitisticki rjesenje 100/7 vrijeme je: ",vrijeme/10)
    
    
    #1000/7
    vrijeme=0
    ACO14=[]
    for i in range(10):
        start=time.time()
        ACO14.append(elitistickiACO(funkcijaCilja,x0,W1,7,1000,1,3,0.5,7))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo elitisticki rjesenje 1000/7 je: ",ACO14)
    print("Prvo elitisticki rjesenje 1000/7 vrijeme je: ",vrijeme/10)
    
    
    #2000/7
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W1,7,2000,1,3,0.5,7))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo elitisticki rjesenje 2000/7 je: ",ACO15)
    print("Prvo elitisticki rjesenje 2000/7 vrijeme je: ",vrijeme/10)
    
    
    
    
    #MATRICA W2
    x0=greedy(W2,0)
    #obicni ACO
    #100/5
    vrijeme=0
    ACO10=[]
    for i in range(10):
        start=time.time()
        ACO10.append(ACO(funkcijaCilja,x0,W2,5,100,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo rjesenje 100/5 je: ",ACO10)
    print("Drugo rjesenje 100/5 vrijeme je: ",vrijeme/10)
    
    #1000/5
    vrijeme=0
    ACO11=[]
    for i in range(10):
        start=time.time()
        ACO11.append(ACO(funkcijaCilja,x0,W2,5,1000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo rjesenje 1000/5 je: ",ACO11)
    print("Drugo rjesenje 1000/5 vrijeme je: ",vrijeme/10)
    
    #2000/5
    vrijeme=0
    ACO12=[]
    for i in range(10):
        start=time.time()
        ACO12.append(ACO(funkcijaCilja,x0,W2,5,2000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo rjesenje 2000/5 je: ",ACO12)
    print("Drugo rjesenje 2000/5 vrijeme je: ",vrijeme/10)
    
    #100/13
    vrijeme=0
    ACO13=[]
    for i in range(10):
        start=time.time()
        ACO13.append(ACO(funkcijaCilja,x0,W2,13,100,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo rjesenje 100/13 je: ",ACO13)
    print("\rvo rjesenje 100/13 vrijeme je: ",vrijeme/10)
    
    
    #1000/13
    vrijeme=0
    ACO14=[]
    for i in range(10):
        start=time.time()
        ACO14.append(ACO(funkcijaCilja,x0,W2,13,1000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo rjesenje 1000/13 je: ",ACO14)
    print("Drugo rjesenje 1000/13 vrijeme je: ",vrijeme/10)
    
    
    #2000/13
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W2,13,2000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo rjesenje 2000/13 je: ",ACO15)
    print("Drugo rjesenje 2000/13 vrijeme je: ",vrijeme/10)
    
    
    
    
    
    
    #elitisticki ACO
    #100/5
    vrijeme=0
    ACO10=[]
    for i in range(10):
        start=time.time()
        ACO10.append(elitistickiACO(funkcijaCilja,x0,W2,5,100,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo elitisticki rjesenje 100/5 je: ",ACO10)
    print("Drugo elitisticki rjesenje 100/5 vrijeme je: ",vrijeme/10)
    
    #1000/5
    vrijeme=0
    ACO11=[]
    for i in range(10):
        start=time.time()
        ACO11.append(elitistickiACO(funkcijaCilja,x0,W2,5,1000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo elitisticki rjesenje 1000/5 je: ",ACO11)
    print("Drugo elitisticki rjesenje 1000/5 vrijeme je: ",vrijeme/10)
    
    #2000/5
    vrijeme=0
    ACO12=[]
    for i in range(10):
        start=time.time()
        ACO12.append(elitistickiACO(funkcijaCilja,x0,W2,5,2000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo elitisticki rjesenje 2000/5 je: ",ACO12)
    print("Drugo elitisticki rjesenje 2000/5 vrijeme je: ",vrijeme/10)
    
    #100/13
    vrijeme=0
    ACO13=[]
    for i in range(10):
        start=time.time()
        ACO13.append(elitistickiACO(funkcijaCilja,x0,W2,13,100,1,3,0.5,13))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo elitisticki rjesenje 100/13 je: ",ACO13)
    print("\rvo elitisticki rjesenje 100/13 vrijeme je: ",vrijeme/10)
    
    
    #1000/13
    vrijeme=0
    ACO14=[]
    for i in range(10):
        start=time.time()
        ACO14.append(elitistickiACO(funkcijaCilja,x0,W2,13,1000,1,3,0.5,13))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo elitisticki rjesenje 1000/13 je: ",ACO14)
    print("Drugo elitisticki rjesenje 1000/13 vrijeme je: ",vrijeme/10)
    
    
    #2000/13
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W2,13,2000,1,3,0.5,13))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo elitisticki rjesenje 2000/13 je: ",ACO15)
    print("Drugo elitisticki rjesenje 2000/13 vrijeme je: ",vrijeme/10)
    
    
    
    #MATRICA W3
    x0=greedy(W3,0)
    #obicni ACO
    #100/5
    vrijeme=0
    ACO10=[]
    for i in range(10):
        start=time.time()
        ACO10.append(ACO(funkcijaCilja,x0,W3,5,100,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece rjesenje 100/5 je: ",ACO10)
    print("Trece rjesenje 100/5 vrijeme je: ",vrijeme/10)
    
    #1000/5
    vrijeme=0
    ACO11=[]
    for i in range(10):
        start=time.time()
        ACO11.append(ACO(funkcijaCilja,x0,W3,5,1000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece rjesenje 1000/5 je: ",ACO11)
    print("Trece rjesenje 1000/5 vrijeme je: ",vrijeme/10)
    
    #2000/5
    vrijeme=0
    ACO12=[]
    for i in range(10):
        start=time.time()
        ACO12.append(ACO(funkcijaCilja,x0,W3,5,2000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece rjesenje 2000/5 je: ",ACO12)
    print("Trece rjesenje 2000/5 vrijeme je: ",vrijeme/10)
    
    #100/17
    vrijeme=0
    ACO17=[]
    for i in range(10):
        start=time.time()
        ACO17.append(ACO(funkcijaCilja,x0,W3,17,100,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece rjesenje 100/17 je: ",ACO17)
    print("\rvo rjesenje 100/17 vrijeme je: ",vrijeme/10)
    
    
    #1000/17
    vrijeme=0
    ACO14=[]
    for i in range(10):
        start=time.time()
        ACO14.append(ACO(funkcijaCilja,x0,W3,17,1000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece rjesenje 1000/17 je: ",ACO14)
    print("Trece rjesenje 1000/17 vrijeme je: ",vrijeme/10)
    
    
    #2000/17
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W3,17,2000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece rjesenje 2000/17 je: ",ACO15)
    print("Trece rjesenje 2000/17 vrijeme je: ",vrijeme/10)
    
    
    
    
    
    
    #elitisticki ACO
    #100/5
    vrijeme=0
    ACO10=[]
    for i in range(10):
        start=time.time()
        ACO10.append(elitistickiACO(funkcijaCilja,x0,W3,5,100,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece elitisticki rjesenje 100/5 je: ",ACO10)
    print("Trece elitisticki rjesenje 100/5 vrijeme je: ",vrijeme/10)
    
    #1000/5
    vrijeme=0
    ACO11=[]
    for i in range(10):
        start=time.time()
        ACO11.append(elitistickiACO(funkcijaCilja,x0,W3,5,1000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece elitisticki rjesenje 1000/5 je: ",ACO11)
    print("Trece elitisticki rjesenje 1000/5 vrijeme je: ",vrijeme/10)
    
    #2000/5
    vrijeme=0
    ACO12=[]
    for i in range(10):
        start=time.time()
        ACO12.append(elitistickiACO(funkcijaCilja,x0,W3,5,2000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece elitisticki rjesenje 2000/5 je: ",ACO12)
    print("Trece elitisticki rjesenje 2000/5 vrijeme je: ",vrijeme/10)
    
    #100/17
    vrijeme=0
    ACO17=[]
    for i in range(10):
        start=time.time()
        ACO17.append(elitistickiACO(funkcijaCilja,x0,W3,17,100,1,3,0.5,17))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece elitisticki rjesenje 100/17 je: ",ACO17)
    print("\rvo elitisticki rjesenje 100/17 vrijeme je: ",vrijeme/10)
    
    
    #1000/17
    vrijeme=0
    ACO14=[]
    for i in range(10):
        start=time.time()
        ACO14.append(elitistickiACO(funkcijaCilja,x0,W3,17,1000,1,3,0.5,17))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece elitisticki rjesenje 1000/17 je: ",ACO14)
    print("Trece elitisticki rjesenje 1000/17 vrijeme je: ",vrijeme/10)
    
    
    #2000/17
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W3,17,2000,1,3,0.5,17))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece elitisticki rjesenje 2000/17 je: ",ACO15)
    print("Trece elitisticki rjesenje 2000/17 vrijeme je: ",vrijeme/10)
    
    
    
    
    
    
    #MATRICA W4
    x0=greedy(W4,0)
    #obicni ACO
    #100/5
    vrijeme=0
    ACO10=[]
    for i in range(10):
        start=time.time()
        ACO10.append(ACO(funkcijaCilja,x0,W4,5,100,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto rjesenje 100/5 je: ",ACO10)
    print("Cetvrto rjesenje 100/5 vrijeme je: ",vrijeme/10)
    
    #1000/5
    vrijeme=0
    ACO11=[]
    for i in range(10):
        start=time.time()
        ACO11.append(ACO(funkcijaCilja,x0,W4,5,1000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto rjesenje 1000/5 je: ",ACO11)
    print("Cetvrto rjesenje 1000/5 vrijeme je: ",vrijeme/10)
    
    #2000/5
    vrijeme=0
    ACO12=[]
    for i in range(10):
        start=time.time()
        ACO12.append(ACO(funkcijaCilja,x0,W4,5,2000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto rjesenje 2000/5 je: ",ACO12)
    print("Cetvrto rjesenje 2000/5 vrijeme je: ",vrijeme/10)
    
    #100/26
    vrijeme=0
    ACO26=[]
    for i in range(10):
        start=time.time()
        ACO26.append(ACO(funkcijaCilja,x0,W4,26,100,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto rjesenje 100/26 je: ",ACO26)
    print("\rvo rjesenje 100/26 vrijeme je: ",vrijeme/10)
    
    
    #1000/26
    vrijeme=0
    ACO14=[]
    for i in range(10):
        start=time.time()
        ACO14.append(ACO(funkcijaCilja,x0,W4,26,1000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto rjesenje 1000/26 je: ",ACO14)
    print("Cetvrto rjesenje 1000/26 vrijeme je: ",vrijeme/10)
    
    
    #2000/26
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W4,26,2000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto rjesenje 2000/26 je: ",ACO15)
    print("Cetvrto rjesenje 2000/26 vrijeme je: ",vrijeme/10)
    
    
    
    
    
    
    #elitisticki ACO
    #100/5
    vrijeme=0
    ACO10=[]
    for i in range(10):
        start=time.time()
        ACO10.append(elitistickiACO(funkcijaCilja,x0,W4,5,100,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto elitisticki rjesenje 100/5 je: ",ACO10)
    print("Cetvrto elitisticki rjesenje 100/5 vrijeme je: ",vrijeme/10)
    
    #1000/5
    vrijeme=0
    ACO11=[]
    for i in range(10):
        start=time.time()
        ACO11.append(elitistickiACO(funkcijaCilja,x0,W4,5,1000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto elitisticki rjesenje 1000/5 je: ",ACO11)
    print("Cetvrto elitisticki rjesenje 1000/5 vrijeme je: ",vrijeme/10)
    
    #2000/5
    vrijeme=0
    ACO12=[]
    for i in range(10):
        start=time.time()
        ACO12.append(elitistickiACO(funkcijaCilja,x0,W4,5,2000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto elitisticki rjesenje 2000/5 je: ",ACO12)
    print("Cetvrto elitisticki rjesenje 2000/5 vrijeme je: ",vrijeme/10)
    
    #100/26
    vrijeme=0
    ACO26=[]
    for i in range(10):
        start=time.time()
        ACO26.append(elitistickiACO(funkcijaCilja,x0,W4,26,100,1,3,0.5,26))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto elitisticki rjesenje 100/26 je: ",ACO26)
    print("\rvo elitisticki rjesenje 100/26 vrijeme je: ",vrijeme/10)
    
    
    #1000/26
    vrijeme=0
    ACO14=[]
    for i in range(10):
        start=time.time()
        ACO14.append(elitistickiACO(funkcijaCilja,x0,W4,26,1000,1,3,0.5,26))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto elitisticki rjesenje 1000/26 je: ",ACO14)
    print("Cetvrto elitisticki rjesenje 1000/26 vrijeme je: ",vrijeme/10)
    
    
    #2000/26
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W4,26,2000,1,3,0.5,26))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto elitisticki rjesenje 2000/26 je: ",ACO15)
    print("Cetvrto elitisticki rjesenje 2000/26 vrijeme je: ",vrijeme/10)
    
    
    
    
    
    
    
    #MATRICA W5
    x0=greedy(W5,0)
    #obicni ACO
    #100/5
    vrijeme=0
    ACO10=[]
    for i in range(10):
        start=time.time()
        ACO10.append(ACO(funkcijaCilja,x0,W5,5,100,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto rjesenje 100/5 je: ",ACO10)
    print("Peto rjesenje 100/5 vrijeme je: ",vrijeme/10)
    
    #1000/5
    vrijeme=0
    ACO11=[]
    for i in range(10):
        start=time.time()
        ACO11.append(ACO(funkcijaCilja,x0,W5,5,1000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto rjesenje 1000/5 je: ",ACO11)
    print("Peto rjesenje 1000/5 vrijeme je: ",vrijeme/10)
    
    #2000/5
    vrijeme=0
    ACO12=[]
    for i in range(10):
        start=time.time()
        ACO12.append(ACO(funkcijaCilja,x0,W5,5,2000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto rjesenje 2000/5 je: ",ACO12)
    print("Peto rjesenje 2000/5 vrijeme je: ",vrijeme/10)
    
    #100/29
    vrijeme=0
    ACO29=[]
    for i in range(10):
        start=time.time()
        ACO29.append(ACO(funkcijaCilja,x0,W5,29,100,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto rjesenje 100/29 je: ",ACO29)
    print("\rvo rjesenje 100/29 vrijeme je: ",vrijeme/10)
    
    
    #1000/29
    vrijeme=0
    ACO14=[]
    for i in range(10):
        start=time.time()
        ACO14.append(ACO(funkcijaCilja,x0,W5,29,1000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto rjesenje 1000/29 je: ",ACO14)
    print("Peto rjesenje 1000/29 vrijeme je: ",vrijeme/10)
    
    
    #2000/29
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W5,29,2000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto rjesenje 2000/29 je: ",ACO15)
    print("Peto rjesenje 2000/29 vrijeme je: ",vrijeme/10)
    
    
    
    
    
    
    #elitisticki ACO
    #100/5
    vrijeme=0
    ACO10=[]
    for i in range(10):
        start=time.time()
        ACO10.append(elitistickiACO(funkcijaCilja,x0,W5,5,100,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto elitisticki rjesenje 100/5 je: ",ACO10)
    print("Peto elitisticki rjesenje 100/5 vrijeme je: ",vrijeme/10)
    
    #1000/5
    vrijeme=0
    ACO11=[]
    for i in range(10):
        start=time.time()
        ACO11.append(elitistickiACO(funkcijaCilja,x0,W5,5,1000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto elitisticki rjesenje 1000/5 je: ",ACO11)
    print("Peto elitisticki rjesenje 1000/5 vrijeme je: ",vrijeme/10)
    
    #2000/5
    vrijeme=0
    ACO12=[]
    for i in range(10):
        start=time.time()
        ACO12.append(elitistickiACO(funkcijaCilja,x0,W5,5,2000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto elitisticki rjesenje 2000/5 je: ",ACO12)
    print("Peto elitisticki rjesenje 2000/5 vrijeme je: ",vrijeme/10)
    
    #100/29
    vrijeme=0
    ACO29=[]
    for i in range(10):
        start=time.time()
        ACO29.append(elitistickiACO(funkcijaCilja,x0,W5,29,100,1,3,0.5,29))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto elitisticki rjesenje 100/29 je: ",ACO29)
    print("\rvo elitisticki rjesenje 100/29 vrijeme je: ",vrijeme/10)
    
    
    #1000/29
    vrijeme=0
    ACO14=[]
    for i in range(10):
        start=time.time()
        ACO14.append(elitistickiACO(funkcijaCilja,x0,W5,29,1000,1,3,0.5,29))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto elitisticki rjesenje 1000/29 je: ",ACO14)
    print("Peto elitisticki rjesenje 1000/29 vrijeme je: ",vrijeme/10)
    
    
    #2000/29
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W5,29,2000,1,3,0.5,29))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto elitisticki rjesenje 2000/29 je: ",ACO15)
    print("Peto elitisticki rjesenje 2000/29 vrijeme je: ",vrijeme/10)
    
    
    
    
    x0=greedy(W1,0)
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W1,5,3000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo rjesenje 3000/5 je: ",ACO15)
    print("Prvo rjesenje 3000/5 vrijeme je: ",vrijeme/10)
    
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W1,7,3000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo rjesenje 3000/7 je: ",ACO15)
    print("Prvo rjesenje 3000/7 vrijeme je: ",vrijeme/10)
       
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W1,5,3000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo elitisticki rjesenje 3000/5 je: ",ACO15)
    print("Prvo elitisticki rjesenje 3000/5 vrijeme je: ",vrijeme/10)
    
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W1,7,3000,1,3,0.5,7))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPrvo elitisticki rjesenje 3000/7 je: ",ACO15)
    print("Prvo elitisticki rjesenje 3000/7 vrijeme je: ",vrijeme/10)
    
    
    
    
    
    
    
    
    x0=greedy(W2,0)
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W2,5,3000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo rjesenje 3000/5 je: ",ACO15)
    print("Drugo rjesenje 3000/5 vrijeme je: ",vrijeme/10)
    
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W2,13,3000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo rjesenje 3000/13 je: ",ACO15)
    print("Drugo rjesenje 3000/13 vrijeme je: ",vrijeme/10)
       
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W2,5,3000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo elitisticki rjesenje 3000/5 je: ",ACO15)
    print("Drugo elitisticki rjesenje 3000/5 vrijeme je: ",vrijeme/10)
    
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W2,13,3000,1,3,0.5,13))
        stop=time.time()
        vrijeme+=stop-start
    print("\nDrugo elitisticki rjesenje 3000/13 je: ",ACO15)
    print("Drugo elitisticki rjesenje 3000/13 vrijeme je: ",vrijeme/10)
    
    
    
    
    
    
    
    
    x0=greedy(W3,0)
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W3,5,3000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece rjesenje 3000/5 je: ",ACO15)
    print("Trece rjesenje 3000/5 vrijeme je: ",vrijeme/10)
    
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W3,17,3000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece rjesenje 3000/17 je: ",ACO15)
    print("Trece rjesenje 3000/17 vrijeme je: ",vrijeme/10)
       
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W3,5,3000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece elitisticki rjesenje 3000/5 je: ",ACO15)
    print("Trece elitisticki rjesenje 3000/5 vrijeme je: ",vrijeme/10)
    
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W3,17,3000,1,3,0.5,17))
        stop=time.time()
        vrijeme+=stop-start
    print("\nTrece elitisticki rjesenje 3000/17 je: ",ACO15)
    print("Trece elitisticki rjesenje 3000/17 vrijeme je: ",vrijeme/10)
    
    
    
    
    x0=greedy(W4,0)
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W4,5,3000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto rjesenje 3000/5 je: ",ACO15)
    print("Cetvrto rjesenje 3000/5 vrijeme je: ",vrijeme/10)
    
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W4,26,3000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto rjesenje 3000/26 je: ",ACO15)
    print("Cetvrto rjesenje 3000/26 vrijeme je: ",vrijeme/10)
       
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W4,5,3000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto elitisticki rjesenje 3000/5 je: ",ACO15)
    print("Cetvrto elitisticki rjesenje 3000/5 vrijeme je: ",vrijeme/10)
    
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W4,26,3000,1,3,0.5,26))
        stop=time.time()
        vrijeme+=stop-start
    print("\nCetvrto elitisticki rjesenje 3000/26 je: ",ACO15)
    print("Cetvrto elitisticki rjesenje 3000/26 vrijeme je: ",vrijeme/10)
    
    
    x0=greedy(W5,0)
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W5,5,3000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto rjesenje 3000/5 je: ",ACO15)
    print("Peto rjesenje 3000/5 vrijeme je: ",vrijeme/10)
    
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(ACO(funkcijaCilja,x0,W5,29,3000,1,3,0.5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto rjesenje 3000/29 je: ",ACO15)
    print("Peto rjesenje 3000/29 vrijeme je: ",vrijeme/10)
       
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W5,5,3000,1,3,0.5,5))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto elitisticki rjesenje 3000/5 je: ",ACO15)
    print("Peto elitisticki rjesenje 3000/5 vrijeme je: ",vrijeme/10)
    
    
    vrijeme=0
    ACO15=[]
    for i in range(10):
        start=time.time()
        ACO15.append(elitistickiACO(funkcijaCilja,x0,W5,29,3000,1,3,0.5,29))
        stop=time.time()
        vrijeme+=stop-start
    print("\nPeto elitisticki rjesenje 3000/29 je: ",ACO15)
    print("Peto elitisticki rjesenje 3000/29 vrijeme je: ",vrijeme/10)
    
    
    graf=[(1150,1760),(630.0,  1660.0),
    (40.0,  2090.0),
    (750.0,  1100.0),
    (750.0,  2030.0),
    (1030.0,  2070.0),
    (1650.0,   650.0),
    (1490.0,  1630.0),
    (790.0,  2260.0),
    (710.0,  1310.0),
    (840.0,   550.0),
    (1170.0,  2300.0),
    (970.0,  1340.0),
    (510.0,   700.0),
    (750.0,   900.0),
    (1280.0,  1200.0),
    (230.0,   590.0),
    (460.0,   860.0),
    (1040.0,   950.0),
    (590.0,  1390.0),
    (830.0,  1770.0),
    (490.0,   500.0),
    (1840.0,  1240.0),
    (1260.0,  1500.0),
    (1280.0,   790.0),
    (490.0,  2130.0),
    (1460.0,  1420.0),
    (1260.0,  1910.0),
    (360.0,  1980.0)]
    rezultat=[1, 28, 6, 12, 9, 5, 26, 29, 3, 2, 21, 20, 10, 4, 15, 18, 17, 14, 22, 11, 19, 13, 16, 25, 7, 23, 27, 8, 24]
    rezultat1=[1,28,6,12,9,5,26,29,3,2,20,10,4,15,18,17,14,22,11,19,25,7,23,27,8,24,16,13,21]#optimalno
    rezultat1=[14, 18, 15, 4, 10, 20, 21, 2, 3, 29, 26, 5, 9, 12, 6, 28, 1, 8, 27, 24, 13, 16, 23, 7, 25, 19, 11, 22, 17]#ACO
    for i in range(len(rezultat)):
        rezultat[i]-=1
    #plot(graf,rezultat)
    
    for i in range(len(rezultat1)):
        rezultat1[i]-=1
    #plot(graf,rezultat1)
    
    rezultati2=[1, 28, 6, 12, 9, 5, 26, 29, 3, 2, 21, 20, 10, 4, 15, 18, 17, 14, 22, 11, 19, 13, 24, 8, 27, 23, 7, 25, 16]#GA
    for i in range(len(rezultati2)):
        rezultati2[i]-=1
    plot(graf,rezultati2)
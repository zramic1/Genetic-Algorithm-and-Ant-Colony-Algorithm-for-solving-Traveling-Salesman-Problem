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
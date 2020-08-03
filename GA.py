# -*- coding: utf-8 -*-
import math as m
import random as r
import time

RANG_SP = 1.5

def funkcijaCilja(cvorovi, matrica):
    suma = 0
    for i in range(len(cvorovi)-1):
        suma += matrica[cvorovi[i]-1][cvorovi[i+1]-1]
    suma += matrica[cvorovi[len(cvorovi)-1]-1][cvorovi[0]-1]
    return suma

def greedyTSP(matrica):
    lista = []
    lista.append(1)
    brojac = 0
    while brojac != len(matrica)-1:
        minimalni = m.inf
        indeks = -1
        for i in range(1, len(matrica[0]) + 1):
            if i not in lista:
                if minimalni > matrica[lista[brojac]-1][i-1]:
                    minimalni =  matrica[lista[brojac]-1][i-1]
                    indeks = i
        lista.append(indeks)
        brojac += 1
    return lista

def formirajOkolinu(cvorovi):
    okolina = []
    for i in range(len(cvorovi)):
        for j in range(i+1,len(cvorovi)):
            nova = [x for x in cvorovi]
            temp = nova[i]
            nova[i] = nova[j]
            nova[j] = temp
            okolina.append(nova)
    return okolina

def generisiOkolinu(duzina):
    cvorovi = []
    for i in range(duzina):
        cvorovi.append(i+1)
    return formirajOkolinu(cvorovi)

def sortiraj(p):
    populacija = []
    sortiraniIndeksi = []
    j = 0
    fa = []
    for i in p:
        populacija.append(i.GetFitness())
        sortiraniIndeksi.append(j)
        fa.append(0)
        j = j + 1
    for it in range(len(populacija)-1,0,-1):
        for i in range(it):
            if populacija[i] > populacija[i+1]:
                temp = populacija[i]
                populacija[i] = populacija[i+1]
                populacija[i+1] = temp

                temp = sortiraniIndeksi[i]
                sortiraniIndeksi[i] = sortiraniIndeksi[i+1]
                sortiraniIndeksi[i+1] = temp
    return populacija, sortiraniIndeksi, fa

class ApstraktnaIndividua(object):

    def SetDuzinaHromozoma(self,DuzinaHromozoma):
        if type(DuzinaHromozoma) is not int:
            raise Exception ("Duzina hromozoma mora biti cijeli broj.")
        self.DuzinaHromozoma = DuzinaHromozoma

    def SetHromozom(self,Hromozom):
        if(len(Hromozom) != self.DuzinaHromozoma):
            raise Exception ("Duzina hromozoma nije ista kao parametar.")
        self.Hromozom = Hromozom

    def SetFitness(self,Fitness):
        self.Fitness = Fitness

    def GetDuzinaHromozoma(self):
        return self.DuzinaHromozoma

    def GetHromozom(self):
        return self.Hromozom

    def GetFitness(self):
        return self.Fitness

    def __init__(self, DuzinaHromozoma, W):
        if type(DuzinaHromozoma) is not int:
            raise Exception ("Duzina hromozoma mora biti cijeli broj.")

        self.DuzinaHromozoma = DuzinaHromozoma
        self.W = W
        okolina = generisiOkolinu(DuzinaHromozoma)
        indeks = r.randint(0,len(okolina)-1)
        u = r.uniform(0,1)
        if(u >= 0.4):
           self.Hromozom = greedyTSP(W)
        else:
            self.Hromozom = okolina[indeks]
        self.Fitness = self.Evaluiraj(funkcijaCilja, self.W)

    def Evaluiraj(self,y):
        pass


maxFit = 100000
cvorovi = []

class MojaIndividua(ApstraktnaIndividua):

    def Evaluiraj(self, f, W):
        global maxFit
        hromozom = self.GetHromozom()

        fit = f(hromozom, W)
        if fit < maxFit:
            maxFit = fit

        return fit

class Populacija(object):

    Populacija = []

    def SetVelicinaPopulacije(self, VelicinaPopulacije):
        if type(VelicinaPopulacije) is not int:
            raise Exception ("Velicina populacije mora biti cijeli broj.")
        self.VelicinaPopulacije = VelicinaPopulacije

    def SetVjerovatnocaUkrstanja(self, VjerovatnocaUkrstanja):
        if (VjerovatnocaUkrstanja<0 or VjerovatnocaUkrstanja>1):
            raise Exception ("Vjerovatnoća mora biti između 0 i 1.")
        self.VjerovatnocaUkrstanja = VjerovatnocaUkrstanja

    def SetVjerovatnocaMutacije(self, VjerovatnocaMutacije):
        if (VjerovatnocaMutacije<0 or VjerovatnocaMutacije>1):
            raise Exception ("Vjerovatnoća mora biti između 0 i 1.")
        self.VjerovatnocaMutacije = VjerovatnocaMutacije

    def SetMaxGeneracija(self, MaxGeneracija):
        if type(MaxGeneracija) is not int:
            raise Exception ("Max Generacija mora biti cijeli broj.")
        self.MaxGeneracija = MaxGeneracija

    def SetVelicinaElite(self, VelicinaElite):
        self.VelicinaElite = VelicinaElite

    def GetVelicinaPopulacije(self):
        return self.VelicinaPopulacije

    def GetVjerovatnocaUkrstanja(self):
        return self.VjerovatnocaUkrstanja

    def GetVjerovatnocaMutacije(self):
        return self.VjerovatnocaMutacije

    def GetMaxGeneracija(self):
        return self.MaxGeneracija

    def GetVelicinaElite(self):
        return self.VelicinaElite

    def GetPopulacija(self):
        return self.Populacija

    def SetPopulacija(self,populacija):
        self.Populacija = populacija

    def __init__(self, W, VelicinaPopulacije, VjerovatnocaUkrstanja, VjerovatnocaMutacije, MaxGeneracija, VelicinaElite, DuzinaHromozoma = 16):
        if type(VelicinaPopulacije) is not int:
            raise Exception ("Velicina populacije mora biti cijeli broj.")
        self.VelicinaPopulacije = VelicinaPopulacije
        if (VjerovatnocaUkrstanja<0 or VjerovatnocaUkrstanja>1) or (VjerovatnocaMutacije<0 or VjerovatnocaMutacije>1):
            raise Exception ("Vjerovatnoća mora biti između 0 i 1.")
        if type(MaxGeneracija) is not int:
            raise Exception ("Max Generacija mora biti cijeli broj.")

        self.VelicinaPopulacije = VelicinaPopulacije
        self.VjerovatnocaUkrstanja = VjerovatnocaUkrstanja
        self.VjerovatnocaMutacije = VjerovatnocaMutacije
        self.MaxGeneracija = MaxGeneracija
        self.VelicinaElite = VelicinaElite
        self.DuzinaHromozoma = DuzinaHromozoma
        self.W = W
        niz = []
        for i in range(self.VelicinaPopulacije):
            individua = MojaIndividua(DuzinaHromozoma, self.W)
            niz.append(individua)
        self.SetPopulacija(niz)

    def OpUkrstanjaDvijeTacke(self, i1, i2):
        h1 = i1.GetHromozom()
        h2 = i2.GetHromozom()

        hromozom1 = []
        hromozom2 = []
        r1 = r.randint(0, self.DuzinaHromozoma-3)
        r2 = r.randint(r1, self.DuzinaHromozoma-2)

        niz1 = []
        niz2 = []
        for i in range(r1, r2+1):
            niz1.append(h1[i])
            niz2.append(h2[i])

        for i in range(self.DuzinaHromozoma):
            if i < r1 or i > r2:
                if h1[i] not in niz2 and h1[i] not in hromozom1:
                    hromozom1.append(h1[i])
                elif h2[i] not in niz2 and h2[i] not in hromozom1:
                    hromozom1.append(h2[i])
                else:
                    k = 0
                    while(h1[k] in niz2 or h1[k] in hromozom1):
                        k += 1
                    hromozom1.append(h1[k])

                if h2[i] not in niz1 and h2[i] not in hromozom2:
                    hromozom2.append(h2[i])
                elif h1[i] not in niz1 and h1[i] not in hromozom2:
                    hromozom2.append(h1[i])
                else:
                    k = 0
                    while(h2[k] in niz1 or h2[k] in hromozom2):
                        k += 1
                    hromozom2.append(h2[k])
            else:
                hromozom1.append(niz2[i-r1])
                hromozom2.append(niz1[i-r1])


        individua1 = MojaIndividua(self.DuzinaHromozoma, self.W)
        individua1.SetHromozom(hromozom1)

        individua2 = MojaIndividua(self.DuzinaHromozoma, self.W)
        individua2.SetHromozom(hromozom2)

        return individua1, individua2

    def OpMutacije(self, individua):
        h = individua.GetHromozom()
        hromozom = [x for x in h]

        i = r.randint(0, self.DuzinaHromozoma-1)
        j = i
        while(j == i):
            j = r.randint(0,self.DuzinaHromozoma-1)

        temp = hromozom[i]
        hromozom[i] = hromozom[j]
        hromozom[j] = temp

        individua = MojaIndividua(self.DuzinaHromozoma, self.W)
        individua.SetHromozom(hromozom)

        return individua

    def SelekcijaRTocak(self):
        populacija = self.GetPopulacija()

        j = 0
        p = [x for x in populacija]
        ukupniFitness = 0
        for i in p:
            ukupniFitness = ukupniFitness + i.GetFitness()
        if len(p) != 0:
            suma = p[0].GetFitness()/ukupniFitness
            u = r.uniform(0,1)
            j = 0
            while suma < u:
                j = j + 1
                suma = suma + p[j].GetFitness()/ukupniFitness

        return p[j]

    def NovaGeneracija(self):
        populacija = self.GetPopulacija()
        velPop = self.GetVelicinaPopulacije()

        p = []
        for i in range(velPop):
            p.append(self.SelekcijaRTocak())

        listaS, indeksiS, fS = sortiraj(p)
        l = []
        for i in range(len(p)):
            l.append(p[i])

        for i in range(len(p) - 1):
            u = r.uniform(0, 1)
            if u < self.GetVjerovatnocaUkrstanja():
                p[i], p[i+1] = self.OpUkrstanjaDvijeTacke(l[indeksiS[i]], l[indeksiS[i+1]])

        for i in range(len(p)):
            u = r.uniform(0, 1)
            if u < self.GetVjerovatnocaMutacije():
                p[i] = self.OpMutacije(p[i])

        sort, sortiraniIndeksi, fa = sortiraj(populacija)
        hromozomi = []
        for i in range(self.GetVelicinaElite()):
            if i < len(populacija):
                hromozomi.append(populacija[sortiraniIndeksi[i]])

        li, si, fi = sortiraj(p)
        for i in range(self.GetVelicinaElite()):
            j = si[len(si)-1-i]
            p[j] = hromozomi[i]
        self.SetPopulacija(p)

        for i in range(len(p)):
            p[i].SetFitness(p[i].Evaluiraj(funkcijaCilja, self.W))

        #print(hromozomi[0].GetHromozom(), hromozomi[0].GetFitness())
        self.SetPopulacija(p)

        return self

    def GenerisiGeneracije(self):
        for i in range(0, self.MaxGeneracija):
            #print("Iteracija ", str(i+1), ": ")
            self.NovaGeneracija()

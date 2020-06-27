# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 16:27:16 2020

@author: héctor
"""

import math as mt
from random import random
import numpy as np
import matplotlib . pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


#### Funcion para algoritmo
def f ( x1 , x2 ) :
    #z = (x1-10)**3+(x2-20)**3 ;
    #z = ((x1**2)+x2-11)**2+(x1+(x2**2)-7)**2 ;    #Modificar aqui para cada una de las funciones
    z = (x1-2)**2+(x2-1)**2 ;
    return z;

NoVariables = 2
HMS = 1000 #Harmony Memory Size (Population Number)
bw = 0.3
HMCR=0.7 # Harmony Memory Considering Rate
PAR=0.8 #Pitch Adjustment Rate
MaxItr=10000 #Maximum number of Iteration
Minim=1; #Minimaization or maximizacion de la funcion? si es 1 se minimizara la funcion, y si es 0 se maximizara la funcion
minim = -10
maxim = 10
minim2 = -10
maxim2 = 10
HM = [  ]
HM2 = [  ]
HF = [  ]
kk = []
yy = []
contador = 0
rango = maxim - minim
rango2 = maxim2 - minim2
mejorP = 0

#inicializacion
i=1
for i in range(HMS): #Se crea la memoria de tamaño HMS junto con sus soluciones
    HM.append(random () * rango + minim)
    HM2.append(random () * rango2 + minim2)    
    HF.append(f(HM[i],HM2[i]))
if Minim==1:
    PeorF = np.amax(HF) #va a encontrar el dato maximo de los resultados de la funcion y la localizacion
    PeorLoc = HF.index(max(HF))
elif Minim==0:
    PeorF = np.amin(HF)
    PeorLoc = HF.index(min(HF))

#Bucle de iteraciones
i=0    
while i < MaxItr and contador !=40:
    harmonyIndex1 = int(random () * HMS + 0)-1#selecciona de la memoria que se genero en la inicializacion valores aleatorios para checarlos
    harmonyIndex2 = int(random () * HMS + 0)-1
    harmony1 = HM[harmonyIndex1] #extraer el valor de la armonia de la memoria, ¿esta es mejor?
    harmony2 = HM2[harmonyIndex2]    
    CMMask1 = (random () * 1 + 0) < HMCR # Se comenzara a improvisar una nueva armonia con probabilidad HMCR
    CMMask2 = (random () * 1 + 0) < HMCR
    NHMask1 =(1-CMMask1)
    NHMask2 = (1-CMMask2)
    PAMask1 = ((random () * 1 + 0)<PAR)*(CMMask1) #Se realiza ademas un ajuste de tono PAR y mas abajo se obtiene la nueva armonia
    PAMask2 = ((random () * 1 + 0)<PAR)*(CMMask2) #controlando la perturbacion aplicada a la variable con bw
    CMMask1 = CMMask1*(1-PAMask1)
    CMMask2 = CMMask2*(1-PAMask2)
    NewHarmony1 = CMMask1 * harmony1 + PAMask1 * (harmony1 + bw * (2 * (random () * 1 + 0) - 1)) + NHMask1 * (minim+(maxim-minim) * (random () * 1 + 0))
    NewHarmony2 = CMMask2 * harmony2 + PAMask2 * (harmony2 + bw * (2 * (random () * 1 + 0) - 1)) + NHMask2 * (minim+(maxim-minim) * (random () * 1 + 0))
    FueraDeLimites1=(NewHarmony1>maxim)+(NewHarmony1<minim) #Se revisara si las nuevas armonias no se salieron de los limites establecidos
    FueraDeLimites2=(NewHarmony2>maxim)+(NewHarmony2<minim)
    if FueraDeLimites1==1: #Si se salieron de los limites las nuevas armonias no se tomaran en cuenta y volveran a la antigua armonia
        NewHarmony1=harmony1
    if FueraDeLimites2==1:
        NewHarmony2=harmony2
    NHF=f(NewHarmony1,NewHarmony2) #Se toma el valor resultado de la funcion con las nuevas armonias
    if (NHF<PeorF)and(Minim==1):
        HM[PeorLoc] = NewHarmony1
        HM2[PeorLoc] = NewHarmony2
        HF[PeorLoc] = NHF
        PeorF = np.amax(HF) #va a encontrar el dato maximo de los resultados de la funcion y la localizacion
        PeorLoc = HF.index(max(HF))
        MejorF = np.amin(HF) #va a encontrar el dato minimo de los resultados de la funcion y la localizacion
        MejorLoc = HF.index(min(HF))
    elif (NHF<PeorF)and(Minim==0):
        HM[PeorLoc] = NewHarmony1
        HM2[PeorLoc] = NewHarmony2
        HF[PeorLoc] = NHF
        PeorF = np.amin(HF) #va a encontrar el dato minimo de los resultados de la funcion y la localizacion
        PeorLoc = HF.index(min(HF))
    Mejor1=HM[MejorLoc]
    Mejor2=HM2[MejorLoc]
    #calcular la calidad de la nueva solucion
    kk.append(i)
    yy.append(MejorF)
    if mejorP!=MejorF:
        plt.plot(Mejor2,Mejor1, marker="o", color="red") #Grafica de puntos
    mejorP=MejorF    
    i = i+1
    print ("{:.6f} {:.6f} {:.6f} \t {i}".format(MejorF, Mejor1, Mejor2, i=i) )
        
if Minim==1:
    MejorF = np.amin(HF) #va a encontrar el dato minimo de los resultados de la funcion y la localizacion
    MejorLoc = HF.index(min(HF))
elif Minim==0:
    MejorF = np.amax(HF) #va a encontrar el dato maximo de los resultados de la funcion y la localizacion
    MejorLoc = HF.index(max(HF))
Mejor1=HM[MejorLoc]
Mejor2=HM2[MejorLoc]

print(Mejor1)
print(Mejor2)
print(MejorF)
plt.xlabel("X2")
plt.ylabel("X1")
plt.show()
plt.plot(kk,yy)
plt.show()
#-----------------------GRÁFICA
#Crear figurar
figura = plt.figure()
#Crear ejes 3D
ejes = Axes3D(figura)
#Mostrar imagen

#definir función
def grafica(X,Y):
    #return (X-10)**3+(Y-20)**3
    #return ((X**2)+Y-11)**2+(X+(Y**2)-7)**2 ##Modificar aqui para cada una de las funciones
    return (X-2)**2+(Y-1)**2
#definir límites de las variables X y Y
limiteMinX=-13
limiteMaxX=100
limiteMinY=-0
limiteMaxY=100
#Crear puntos para las variables
X = np.linspace(limiteMinX,limiteMaxX,40)
Y = np.linspace(limiteMinY,limiteMaxY,40)
#Crear malla
X,Y = np.meshgrid(X,Y)
#definir Z
Z = grafica(X,Y)
#superficie
ejes.plot_surface(X, Y, Z, cmap='twilight')
plt.scatter(Mejor1,Mejor2,MejorF, c='r', marker='o')
#nombre de los ejes
ejes.set_xlabel('X axis')
ejes.set_ylabel('Y axis')
ejes.set_zlabel('Z axis') 
plt.show()
        


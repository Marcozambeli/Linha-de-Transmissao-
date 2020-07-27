# -*- coding: utf-8 -*-
"""
Created on Thu May 23 15:08:43 2019


@author: Marcozambeli
"""

import numpy as np #importei bibliot numpy para usar os valores de relevo e chamo suas ferramentas com np
import matplotlib.pyplot as plt#para vizualizar dados no relevo
from libby import equation #importa a equacao que fiz no outro prog
from scipy.optimize import fsolve #importa funcao para solucao de problemas
import math

plt.close('all')#para nao ficarmos td hr fechando manualmente a figura

M = np.loadtxt(open("route.csv","r"),delimiter=",",skiprows=1,usecols=(3,2))#ferramenta para carregarmos dados a partir de um arquivo text, "r" significa somente leitura do arqvo e neste caso, o separador de dados e virgula",", skiprows pula linhas do arqv, quero somente as colunas(0,1,2,3) relativas a elevacao e distancia
#rodo e consigo ver matriz com os dados
M[:,0] = M[:,0]*1000#multiplico todas os itens da 1 coluna (0) por 1000 para transformalos em metros

rmin = 6 #altura minima tabelada para cabo c tensao de 69kv sobre somente pedestres
R = np.array([[200,8],[400,8]])#crio um vetor para altura minima sobre estrada rural,composto por 2 linhas com local e altura minima-na tabela que fiz temos 2 estradas, uma a 200 e outra a 400m (para as 2 altura de 8m)
                #^ aqui add todas as restricoes de atura do problema
y_min = M[:,1] + rmin#tracar uma linha auxiliar para delimitar as alturas minimas onde cada linha pode ficar=relevo+altminima

numlinhasR = np.shape(R)[0] #declarar uma var auxiliar com o numero de restricoes minimas que possuimos para alturas diferenciadas, shape nos retorna as dimensoes da matriz(qro saber no de linhas = 0 = 1a coluna da matrix)

for i in range(0,numlinhasR):#criar um loop para varrer a matriz R e add as restricoes dos locais com alt diferenciadas
    indice = np.where(M[:,0]>R[i,0])[0][0] # retorna tds indices onde essa relacao de > e verdadeira,acho qual elemento da matriz e mais proximo da 1 restricao (a200m)...[0][0]especifica oq eu quero: pega a 1 posicao de cada info e primeira informacao do retorno
    y_min[indice-2:indice+2] = M[indice-2:indice+2,1] + R[i,1] #atualizo o vetor y_min com uma certa margem de seguranca dos lcais das restricoes, R[i,1] significa que a restricao esta na segunda coluna da matrixR

#criar uma figura para tracar as torres, relevo e catenarias
plt.figure(1)
plt.xlabel("x [m]")
plt.ylabel("y [m]")

plt.plot(M[:,0],M[:,1],'b',M[:,0],y_min,'r')#ploto a primeira(0) e a segunda(1) coluna com linha azul e em vermelho a linha aux de altura min

xt1 = 0 #local da primeira torre
xt2 = 300 #indice perto da torre 2 = indice 63
xt3 = 950
xt4 = 1214

H = 20 #altura da torre, de acordo com fabricante
#achar na matrix(tabela)qual indice fica mais proximo a localizacao ds torres
i_t1 = np.where(M[:,0]>=xt1)[0][0] #semelhante a linha 23
i_t2 = np.where(M[:,0]>=xt2)[0][0] #indice da torre 2
i_t3 = np.where(M[:,0]>=xt3)[0][0]
i_t4 = np.where(M[:,0]>=xt4)[0][0]

yt1 = M[i_t1,1] + H #coord y do pt mais alto da torre t1= indice t1 que e a segunda coluna da matrix + atura da torre
yt2 = M[i_t2,1] + H
yt3 = M[i_t3,1] + H
yt4 = M[i_t4,1] + H

T1 = np.array([[xt1,M[i_t1,1]],[xt1,yt1]]) #criar um vetor com as coord da torre, do pt do solo ate o yt1 (pt mais alto da torre1)
T2 = np.array([[xt2,M[i_t2,1]],[xt2,yt2]])
T3 = np.array([[xt3,M[i_t3,1]],[xt3,yt3]])
T4 = np.array([[xt4,M[i_t4,1]],[xt4,yt4]])

plt.plot(T1[:,0], T1[:,1],'k')#ploto todos os pts da primeira coluna do vetor T, o que significa desenhar no grafico a torre
plt.plot(T2[:,0], T2[:,1],'k')
plt.plot(T3[:,0], T3[:,1],'k')
plt.plot(T4[:,0], T4[:,1],'k')

#EQUACAO DA CATENARIA 1
Tnom = 140e3 #rated strenght do cabo escolhido
ms = 1350*9.81/1000#[N/m] peso*gravidade/1000
Tmax = 0.25*Tnom# tracao max que o cabo pode assumir.25% garate que o cabo nao se deforme permanentemente (operacao na regiao elastica)
T0 = 0.95*Tmax #devo alterar esses parametros juntamente com o xtorre

#ativar modo de solucao de equacoes do python, definir equacoes num arquivo a parte

parametros = (xt1,xt2,yt1,yt2,T0,ms) #,mandar para o libby os parametros na msm ordem que foram declarados la
x0 = fsolve(equation,xt1,args=parametros)[0]#xt1=pto inicial, resolve a equacao e retorna x0
y0 = yt1-T0/ms*(math.cosh(ms/T0*(xt1-x0))-1) #subst o valor obtido de x0 em alguma equacao

catenaria1_x = np.arange(xt1-x0,xt2-x0,1) #vetor que contem todas as compoentes x da 1a catenaria, de 1 em 1 metro
catenaria1_y = np.array([T0/ms*(math.cosh(ms/T0*x)-1) for x in catenaria1_x ])#aplico a eq da catenaria para todos os valores de x no vetor catenaria1_x

#mas nao quero a catenaria na origem, mas sim no local real, entao:
catenaria1_x_real = catenaria1_x + x0
catenaria1_y_real = catenaria1_y + y0

plt.plot(catenaria1_x_real, catenaria1_y_real,'m')

#EQUACAO DA CATENARIA 2

parametros = (xt2,xt3,yt2,yt3,T0,ms) #,mandar para o libby os parametros na msm ordem que foram declarados la
x0 = fsolve(equation,xt2,args=parametros)[0]#xt1=pto inicial, resolve a equacao e retorna x0
y0 = yt2-T0/ms*(math.cosh(ms/T0*(xt2-x0))-1) #subst o valor obtido de x0 em alguma equacao

catenaria2_x = np.arange(xt2-x0,xt3-x0,1) #vetor que contem todas as compoentes x da 1a catenaria, de 1 em 1 metro
catenaria2_y = np.array([T0/ms*(math.cosh(ms/T0*x)-1) for x in catenaria2_x ])#aplico a eq da catenaria para todos os valores de x no vetor catenaria1_x

#mas nao quero a catenaria na origem, mas sim no local real, entao:
catenaria2_x_real = catenaria2_x + x0
catenaria2_y_real = catenaria2_y + y0
plt.plot(catenaria2_x_real, catenaria2_y_real,'m')

#EQUACAO DA CATENARIA3

parametros = (xt3,xt4,yt3,yt4,T0,ms) #,mandar para o libby os parametros na msm ordem que foram declarados la
x0 = fsolve(equation,xt3,args=parametros)[0]#xt1=pto inicial, resolve a equacao e retorna x0
y0 = yt3-T0/ms*(math.cosh(ms/T0*(xt3-x0))-1) #subst o valor obtido de x0 em alguma equacao

catenaria3_x = np.arange(xt3-x0,xt4-x0,1) #vetor que contem todas as compoentes x da 1a catenaria, de 1 em 1 metro
catenaria3_y = np.array([T0/ms*(math.cosh(ms/T0*x)-1) for x in catenaria3_x ])#aplico a eq da catenaria para todos os valores de x no vetor catenaria1_x

#mas nao quero a catenaria na origem, mas sim no local real, entao:
catenaria3_x_real = catenaria3_x + x0
catenaria3_y_real = catenaria3_y + y0
plt.plot(catenaria3_x_real, catenaria3_y_real,'m')

#criar uma figura para o grafico de tracao
plt.figure(2)
plt.xlabel("x [m]")
plt.ylabel("Tcabo [N]")
#grafico cat1
T = T0 + catenaria1_y*ms
Vtmax = Tmax*np.ones(len(catenaria1_x_real)) #vetor onde tds posicoes possuem o msm valor

plt.plot(catenaria1_x_real,T, 'b',catenaria1_x_real, Vtmax, 'r')

#grafico cat2
T = T0 + catenaria2_y*ms
Vtmax = Tmax*np.ones(len(catenaria2_x_real)) #vetor onde tds posicoes possuem o msm valor

plt.plot(catenaria2_x_real,T, 'g',catenaria2_x_real, Vtmax, 'r')

#grafico cat3
T = T0 + catenaria3_y*ms
Vtmax = Tmax*np.ones(len(catenaria3_x_real)) #vetor onde tds posicoes possuem o msm valor

plt.plot(catenaria3_x_real,T, 'k',catenaria3_x_real, Vtmax, 'r')


#CALCULO DO COMPRIMENTO DE CABO
S = T0/ms*(math.sinh(ms/T0*(xt4-x0))-math.sinh(ms/T0*(xt1-x0)))
print("comprimento do cabo: ",S,"m")

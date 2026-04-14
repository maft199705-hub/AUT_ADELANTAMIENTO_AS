import pandas as pd
import numpy as np
from pathlib import Path 
import sys
import os
import re


# --- Soporte para PyInstaller ---
if hasattr(sys, "_MEIPASS"):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
    
    
from funciones import funciones

class logica_frecuencias:
    funcion = funciones()
    dias_llamado_num = []
    dias_despacho_num = []
    regla_entrega = 0
    regla = 0
    feriado = [] #siempre se debe de incluir el 0 como dia domingo
    orden = {"L": 0, "M": 1, "W": 2, "J": 3, "V": 4, "S": 5, "D": 6}
    cont = 0
		
    def __init__(self):
        pass
    
#---------------------------------------FUNCIONES---------------------------------------#
#---------------------------    GENERICAS

    def calculo_feriados(self,dia_llamado:int, dia_despacho:int, feriados:list[0]): #Cuenta la cantidad de feriados entre día de llamado y día de despacho
        try:
            self.cont = 0
            
            for i in feriados:
                if dia_llamado < i < dia_despacho:
                    self.cont += 1            
            return self.cont
                    
        except Exception as e:
            print(f'Error: {e} /ERROR CLASS LOGICA_FRECUENCIA: calculo_feriados()')
            
    def not_duplicate(self, lista:list):#elimina duplicados en una lista
        try:
            not_duplicate = []
            for i in lista:
                if i not in not_duplicate:
                    not_duplicate.append(i)
            return not_duplicate
        except Exception as e:
            print(f'Error: {e} /ERROR CLASS LOGICA_FRECUENCIA: not_duplicate()')
            return None
        
#---------------------------    ESPECIFICAS 
    def calculo_llamado_insitu(self,row):
    #(self,dias_llamado_num:list[0], dias_despacho_num:list[0], dias_llamado_insitu_post_num:list[0], feriados:list[0], regla_num:float)   
    # dias_llamado_num_insitu:list[0], dias_despacho_num_insitu:list[0], regla_entrega:float, feriados:list[0])
    #Calculo se hace por linea del df
    #Sistema debe captar día de despacho y por regla de entrega determinar día de llamado
        try:
            dias_llamado_num = row['dias_llamado_num']
            dias_despacho_num = row['dias_despacho_num']
            regla_num = row['regla_num']
            feriados = row['feriados_num']
            dias_llamado_insitu_post_num = row['dias_llamado_insitu_post_num']

            
            dias_llamado_previa_insitu_num = []#lista de  dias de llamado  semana previa calculados en semana insitu
            dias_llamado_insitu_num = [] #lista de dias de llamado en la semana insitu
            dias_despacho_insitu_num = []#lista de dias de despacho en la semana insitu
            
                
            for i in dias_llamado_num: #Descarte del día de llamado y dias de despacho por feriado
                if i not in feriados:
                    dias_llamado_insitu_num.append(i)
            for i in dias_despacho_num:
                if i not in feriados:
                    dias_despacho_insitu_num.append(i)
            
                
            """ if len(dias_llamado_insitu_num) == len(dias_despacho_insitu_num) and dias_llamado_insitu_post_num == []: #Descarte de evaluacion por linea de cliente
                cont = 0
                for i,k in zip(dias_llamado_insitu_num, dias_despacho_insitu_num):                
                    if k - i - self.calculo_feriados(i,k,feriados)>= regla_num:
                        cont += 1
                        
                if cont == len(dias_despacho_insitu_num):
                    return dias_llamado_insitu_num, dias_despacho_insitu_num , dias_llamado_previa_insitu_num #FINALIZA LA FUNCION """
                 
            #Si no existe el descarte del cliente se procede con la creacion de los dias de llamado
            dias_llamado_insitu_num = []  #lista de  dias de llamado vacia    
            for i in dias_despacho_insitu_num: #calcula dia de llamado segun regla de entrega y dia de despacho
                dia_llamado = i - regla_num #dia de llamado propuesto
                                
                while True:
                    if  i - dia_llamado - self.calculo_feriados(dia_llamado, i, feriados) >= regla_num and dia_llamado not in feriados:
                        if dia_llamado < 0:
                            dias_llamado_previa_insitu_num.append(dia_llamado%7) #se aplica aritmetica modular
            
                        else :   
                            dias_llamado_insitu_num.append(dia_llamado)
                           
                        break
                    else:
                        dia_llamado -= 1
             
            if dias_llamado_insitu_post_num == []: #evaluamos posibilidad de descarte si no hay que agregar dias de llamado de la post            
                return dias_llamado_insitu_num, dias_despacho_insitu_num , dias_llamado_previa_insitu_num #FINALIZA LA FUNCION
            else:
                propuesta = dias_llamado_insitu_num + dias_llamado_insitu_post_num # se concatenan todos los dias de la semana insitu
                propuesta = sorted(self.not_duplicate(propuesta)) #eliminamos duplicados y ordenamos en orden ascendente
                dias_llamado_insitu_num = []
                eliminate = []
                for k in propuesta: #eliminamos el siguiente dia si el dia anterior ya fue agregado
                    if k not in eliminate:
                        dias_llamado_insitu_num.append(k)
                        if k+1 in propuesta:
                            eliminate.append(k+1)
                                
            return dias_llamado_insitu_num, dias_despacho_insitu_num , dias_llamado_previa_insitu_num #FINALIZA LA FUNCION                
        except Exception as e:
            print(f'Error: {e} /ERROR CLASS LOGICA_FRECUENCIA: calculo_llamado_insitu()')
            return None
        
    def calculo_llamado_previa(self, row):
        #(self,  dias_despacho_num, dias_llamado_previa_insitu_num, dias_llamado_insitu_num, regla_num)
        #Se descartan lo feriados para concatenar los dias de llamado previa y semana insitu
        try:
            
            dias_despacho_num= row['dias_despacho_num']
            dias_llamado_previa_insitu_num = row['dias_llamado_previa_insitu_num']
            regla_num = row['regla_num']
            
            dias_llamado_previa_num = []#dias de llamado semana previa
            feriados = [0] #solo se considera el domingo como feriado en esta logica            
            
            for i in dias_despacho_num: #calcula dia de llamado segun regla de entrega y dia de despacho sin considerar los feriados
                dia_llamado = i - regla_num #dia de llamado propuesto
                                
                while True:
                    if  i - dia_llamado - self.calculo_feriados(dia_llamado, i, feriados) >= regla_num and dia_llamado not in feriados:
                        if dia_llamado > 0:
                            dias_llamado_previa_num.append(dia_llamado) 
                            
                        break
                    else:
                        dia_llamado -= 1
        
           
            if len(dias_llamado_previa_num) == len(dias_despacho_num) and dias_llamado_previa_insitu_num == []:#Verificamos posibilidad descarte de evaluacion por linea de cliente
                return dias_llamado_previa_num #FINALIZA LA FUNCION
            
            else:
                propuesta = dias_llamado_previa_num + dias_llamado_previa_insitu_num
                propuesta = sorted(self.not_duplicate(propuesta)) #eliminamos duplicados y ordenamos en orden ascendente
                dias_llamado_previa_num = []
                eliminate = []
                for k in propuesta: #eliminamos el siguiente dia si el dia anterior ya fue agregado
                    if k not in eliminate:
                        dias_llamado_previa_num.append(k)
                        if k+1 in propuesta:
                            eliminate.append(k+1)
                                
                return dias_llamado_previa_num #FINALIZA LA FUNCION
        
        except Exception as e:
            print(f'Error: {e} /ERROR CLASS LOGICA_FRECUENCIA: calculo_llamado_previa()')
            return None
        
    def calculo_llamado_post(self, row):
        #(self, dias_despacho_num, feriados_num, regla_num):
        #Calculo de dias de llamado de semana post
        try:
            
            dias_despacho_num = row['dias_despacho_num']
            feriados_num= [0] #solo se considera el domingo como feriado en esta logica
            regla_num = row['regla_num']
            feriados_insitu = row['feriados_num']
            
            dias_llamado_post = []  #dias de llamado semana post
            dias_llamado_insitu_post = [] #dias de llamamado de semana insistu calculados en semana post
            dias_llamado_post_post = [] #dias de llamado de semana post calculados en funcion a despachos de la semana siquiente al post
            
            for i in dias_despacho_num:#calula dia de llamado segun regla de entrega y dia de despacho
                dia_llamado = i - regla_num
                while True:
                    if i - dia_llamado - self.calculo_feriados(dia_llamado, i, feriados_num) >= regla_num and dia_llamado not in feriados_num:
                        if dia_llamado > 0:
                            dias_llamado_post.append(dia_llamado)
                            break
                        elif dia_llamado < 0:
                            dias_llamado_insitu_post.append(dia_llamado%7)
                            dias_llamado_post_post.append(dia_llamado%7)
                            break
                
                    dia_llamado -= 1
            
            propuesta = []
            for i in dias_llamado_insitu_post:#descarte de dias que caeben en feriado / se mueven un dia hacia atras hasta cumplir condicional
                while True:
                    if i not in feriados_insitu:
                        propuesta.append(i)
                        break
                    i -= 1
            
            dias_llamado_insitu_post = propuesta
            
            dias_llamado_post = dias_llamado_post + dias_llamado_post_post #anexamos dias de llamado cuyo despacho es la semana siguiente al post
            dias_llamado_post = sorted(self.not_duplicate(dias_llamado_post)) #eliminamos duplicados y ordenamos en orden ascendente
            
            return dias_llamado_post, dias_llamado_insitu_post #FINALIZA LA FUNCION
            
        except Exception as e:
            print(f'Error: {e} /ERROR CLASS LOGICA_FRECUENCIA: calculo_llamado_post()')
            return None
          
#--------------------------------------  EJECUCION  ---------------------------------# 

""" llamados = [1] #LUNES 
despachos = [3,5] #MIERCOLES Y VIERNES
regla = 1
feriados = [4,5,6,7] #VIERNES

llamados_insitu_post_num = [6]
llamados_previa_insitu_num = [6]

llamados_insitu_num = [3,6]
despachos_insitu_num = [3,5]


ejecutar = logica_frecuencias()
resultado = ejecutar.calculo_llamado_insitu( despachos, llamados_previa_insitu_num, llamados_insitu_num,despachos_insitu_num, regla)
print(resultado)  """


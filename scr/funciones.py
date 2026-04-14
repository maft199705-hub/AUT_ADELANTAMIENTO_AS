import pandas as pd
import numpy as np
from pathlib import Path 


class funciones:
    __archivo = ''
    
    def __init__(self):
        pass
    
#---------------------------------------METODOS---------------------------------------#
    def leer(self, ruta, hoja): #LEE 1 ARCHIVO EXCEL
        try:
            self.__archivo =  pd.read_excel(Path(ruta),sheet_name = hoja)
            return self.__archivo
            
        except Exception as e:
            print(f'Error al leer el archivo: {e} /ERROR CLASS FUNCIONES: leer()')
            return None
    
    def escribir(self, df, ruta, hoja): #ESCRIBE 1 ARCHIVO EXCEL
        try:
            with pd.ExcelWriter(
                Path(ruta),
                engine="openpyxl",
                mode="a",                  # adjuntar al archivo existente
                if_sheet_exists="replace"  # reemplaza la hoja 'Personas'
            ) as writer: df.to_excel(writer, sheet_name=hoja, index=False)
            
        except Exception as e:
            print(f'Error al escribir el archivo: {e} /ERROR CLASS FUNCIONES: escribir()')
            return None
    
    def letra_to_numero (self, valor):  #CONVIERTE LETRAS A NUMEROS
        try:          
            orden = {'D': 0, 'L': 1, 'M': 2, 'W': 3, 'J': 4, 'V': 5, 'S': 6}
            if pd.isna(valor):
                return 'ERROR CLASS READ: letra_to_numero() / valor NULO' 
            
            numero =[]
            for i in valor:
                numero.append(orden[i])
                
            return numero
        except Exception as e:
            print(f'Error: {e} /ERROR CLASS FUNCIONES: letra_to_numero()')
            return None
        
    def numero_to_letra (self, valor):  #COVIERTE DE NUMERO A LETRA
        try:          
            orden = {0: 'D', 1: 'L', 2: 'M', 3: 'W', 4: 'J', 5: 'V', 6: 'S'}
            
            letra =[]
            for i in valor:
                letra.append(orden[i])
            
            letra = ''.join(map(str, letra))
                
            return letra
        except Exception as e:
            print(f'Error: {e} /ERROR CLASS FUNCIONES: numero_to_letra()')
            return None  
     
    def regla_to_num(self,valor):  #CONVIERTE LISTA DE FERIADOS DE LETRAS A NUMEROS
        try:          
            orden = {24: 1, 48: 2, 72: 3}
            if pd.isna(valor):
                return 'ERROR CLASS READ: regla_to_num() / valor NULO' 
            
            numero = orden[valor]

            return numero
        except Exception as e:
            print(f'Error: {e} /ERROR CLASS FUNCIONES: regla_to_num()')
            return None
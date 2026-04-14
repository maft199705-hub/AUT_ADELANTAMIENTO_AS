import pandas as pd
import numpy as np
import sys
import os


# --- Soporte para PyInstaller ---
if hasattr(sys, "_MEIPASS"):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


  
from funciones import funciones

class logica_prioridad:
    funcion = funciones()
    def __init__(self):
        pass
    
#---------------------------------------FUNCIONES---------------------------------------#
#---------------------------    GENERICAS
#---------------------------    ESPECIFICAS 
    def contactabilidad_efectividad(self, ruta, hoja):
        #calcula promedio de contactabilidad por cliente y pasar valor a numero para asignar la prioridad
        try:
            dff_contact_efect = self.funcion.leer(ruta, hoja[4]) #lectura de la hoja RESUMEN CONTACT Y EFECT) 
            dff = self.funcion.leer(ruta, hoja[1]) #lectura de la hoja DATOS PRIORIZACION) 
            
            dff_contact_efect['contactabilidad'] = dff_contact_efect['contactabilidad'] * 20 #transformacion de dato
            dff_contact_efect['efectividad'] = dff_contact_efect['efectividad'] * 35 #transformacion de dato
            
            tallas = {'S':3.75, 'M': 7.5, 'L':11.25, 'XL':15, 'SIN TALLA':2}
            
            dff_contact_efect['talla'] = dff_contact_efect['talla'].map(tallas)#transformacion de dato
            
            dff = dff.merge(dff_contact_efect, on = 'cliente', how = 'left', suffixes = ('_x', '')).drop(columns =['talla_x', 'contactabilidad_x', 'efectividad_x']).fillna(0)
            self.funcion.escribir(dff, ruta, hoja[1])
            
            return 0
        except Exception as e:
            print(f'Error: {e} /ERROR CLASS LOGICA_PRIORIDAD: contactabilidad_efectividad()')
            return None       
       
    def netos_kilos_ultimo(self, ruta, hoja):
        #calcula promedio de netos, kilos y ultima compra por cliente y obtiene el promedio mas alto a nivel nacional para asignar la prioridad
        try:
            dff_pedidos = self.funcion.leer(ruta, hoja[2]) #lectura de la hoja RESUMEN DE PEDIDOS
            dff = self.funcion.leer(ruta, hoja[1]) #lectura de la hoja RESUMEN DE DESCARTES) 
            
            dff_pedidos['fecha'] = pd.to_datetime(dff_pedidos['fecha'], errors = "coerce", dayfirst = True) # conversion de fecha a dato tipo fecha
     
            desde = dff_pedidos.iloc[0,4] #fecha inicio de filtrado
            hasta = desde + pd.DateOffset(months = 6) #fecha final de filtrado
     
            mask = (dff_pedidos['fecha'] >= desde) & (dff_pedidos['fecha'] <= hasta)
            dff_pedidos = dff_pedidos.loc[mask]
            
            #calculo kilos
            dff_pedidos['prom_kilos'] = dff_pedidos.groupby('cliente')['kilos'].transform('mean') # promedio de kilos por cliente
            max_kilos = dff_pedidos['kilos'].max() #calculo del maximo de kilos
            dff_pedidos['kilos'] = dff_pedidos['prom_kilos'] / max_kilos * 10 #transformacion de datos en puntuacion definida
            
            #calculo netos
            dff_pedidos['prom_netos'] = dff_pedidos.groupby('cliente')['netos'].transform('mean') # promedio de netos por cliente
            max_netos = dff_pedidos['netos'].max() #calculo del maximo de netos
            dff_pedidos['netos'] = dff_pedidos['prom_netos'] / max_netos * 20 #transformacion de datos en puntuacion definida
            
            dff_pedidos = dff_pedidos.drop_duplicates(subset=["cliente"], keep="first") #se eliminan duplicados
            
            dff = dff.merge(dff_pedidos, on = 'cliente', how = 'left', suffixes = ('_x', '') ).drop(columns=['netos_x', 'kilos_x','fecha', 'prom_kilos', 'prom_netos', 'fecha inicial', 'fecha final' ]).fillna(0) #cruce por cliente a evaluar  
            
            self.funcion.escribir(dff, ruta, hoja[1]) 
    
            return 0
        
        except Exception as e:
            print(f'Error: {e} /ERROR CLASS LOGICA_PRIORIDAD: netos_kilos_ultimo()')
            return None
            
    def descartes(self, ruta, hoja):
        try:
            dff = self.funcion.leer(ruta, hoja[1]) #lectura de la hoja DATOS PRIORIZACION
            dff_descarte = self.funcion.leer(ruta, hoja[3]) #lectura de la hoja RESUMEN DE DESCARTES
            
            nuevo = dff_descarte['nuevo'].drop_duplicates(keep='first').reset_index(drop=True) #Se crea un nuevo df de nuevos no duplicado
     
            bloqueado = dff_descarte['bloqueado'].drop_duplicates(keep='first').reset_index(drop=True) #Se crea un nuevo df de bloqueado no duplicado
       
            cerrado = dff_descarte['cerrado'].drop_duplicates(keep='first').reset_index(drop=True) #Se crea un nuevo df de cerrado no duplicado
            
            dff = dff.merge( #Se realiza cruce de clientes para llamar con clientes nuevos
                nuevo,
                how='left',               # 'left', 'right', 'inner', 'outer'
                left_on='cliente',      
                right_on='nuevo',
                suffixes=('_x', '')     
            )

            dff = dff.merge( #Se realiza cruce de clientes para llamar con clientes bloqueados
                bloqueado,
                how = 'left',
                left_on = 'cliente',
                right_on = 'bloqueado',
                suffixes = ('_x', '')
            )
            
            dff = dff.merge( #Se realiza cruce de clientes para llamar con clientes cerrados
                cerrado,
                how = 'left',
                left_on = 'cliente',
                right_on = 'cerrado',
                suffixes = ('_x', '')
            )  
                 
            dff = dff.drop(columns = ['nuevo_x', 'bloqueado_x', 'cerrado_x'])   # eliminamos suffixes
            dff = dff.fillna(0).astype(int) #se cambias los vacios por 0
            
            dff.loc[dff['nuevo'] > 0, ['nuevo']] = 1 #se modifican todos por valor 1 equivalente a descartado
            dff.loc[dff['bloqueado'] > 0, ['bloqueado']] = 1
            dff.loc[dff['cerrado'] > 0, ['cerrado']] = 1
            
            self.funcion.escribir(dff, ruta, hoja[1])
            
            return 0
       
        except Exception as e:
            print(f'Error: {e} /ERROR CLASS LOGICA_PRIORIDAD: calculo_prioridad()')
            return None
        
    def comportamiento_compra(self, ruta, hoja):
        try:
            dff_pedidos = self.funcion.leer(ruta, hoja[2]) #lectura de la hoja RESUMEN DE PEDIDOS
            dff = self.funcion.leer(ruta, hoja[1])#lectura de la hoja DATOS PRIORIZACION'

            dff_pedidos['fecha'] = pd.to_datetime(dff_pedidos['fecha'], errors = "coerce", dayfirst = True) # conversion de fecha a dato tipo fecha
            dff_pedidos = dff_pedidos.drop_duplicates(subset = ['cliente','fecha'])
            
            desde = dff_pedidos.iloc[0,4] #fecha inicio de filtrado
            hasta = desde + pd.DateOffset(months = 6) #fecha final de filtrado
     
            mask = (dff_pedidos['fecha'] >= desde) & (dff_pedidos['fecha'] <= hasta)
            dff_pedidos = dff_pedidos.loc[mask]
 
            mes_inicial = desde.month #se captura valor de la fecha inicion
            desfase = mes_inicial - 1 #se calcula el desfase
            
            dff_pedidos = dff_pedidos.drop(columns = ['fecha inicial', 'fecha final']) #se elimina informacion no pertinente
            
            
            dff_pedidos['semana'] = dff_pedidos['fecha'].dt.isocalendar().week
            dff_pedidos['mes'] = dff_pedidos['fecha'].dt.month
            
            
            dff_pedidos['mes'] = dff_pedidos['mes'] - desfase 
            mask = dff_pedidos['mes'] < 0
            dff_pedidos.loc[mask, 'mes'] = dff_pedidos.loc[mask, 'mes'] + 12
            
    
            dff_pedidos['semana'] = dff_pedidos['semana'].fillna(0).astype(int)
            
            dff_pedidos.loc[dff_pedidos['semana'] > 1, 'semana'] = 1 #transformacion de varlores unitarios          
            
            meses = {1:0.1, 2:0.4, 3:0.8, 4:1.2, 5:1.6, 6:2} #se valora mas la cercania a la fecha actual
            dff_pedidos['mes'] = dff_pedidos['mes'].map(meses)
            
            dff_pedidos['semana'] = dff_pedidos['semana'] * dff_pedidos['mes'] # aplicacion de factor de valor mes
            
            pedidos = pd.DataFrame()
            pedidos['comportamiento de compra'] = dff_pedidos.groupby('cliente')['semana'].sum() #se suma puntacion de clientes por mes
            max_comport = pedidos['comportamiento de compra'].max() # se optiene el mejo comportamiento
            pedidos['comportamiento de compra'] = pedidos['comportamiento de compra'] / max_comport *100 # se aplica porcentaje a los valores
            
            dff = dff.merge(pedidos, on = 'cliente', how = 'left', suffixes = ('_x', '')).drop(columns = ['comportamiento de compra_x'])
            dff = dff.fillna(0).astype(int)
            self.funcion.escribir(dff, ruta, hoja[1])
            
            return dff
            
        except Exception as e:
            print(f'Error: {e} /ERROR CLASS LOGICA_PRIORIDAD: comportamiento_compra()')
            return None
  
#--------------------------------------  EJECUCION  ---------------------------------# 
""" ruta = 'C:/Users/moise/Desktop/MY PROYECTS/AUT_ADELANTAMIENTO/adelantamiento.xlsx' #archivo principal
hoja =['DIAS DE LLAMADO', 'DATOS PRIORIZACION', 'RESUMEN DE PEDIDOS', 'RESUMEN DE DESCARTES', 'RESUMEN DE CONTAC Y EFECT']

prioridad = logica_prioridad()

#dff = prioridad.descartes(ruta, hoja)
#dff = prioridad.netos_kilos_ultimo(ruta, hoja) 
#dff= prioridad.contactabilidad_efectividad(ruta, hoja)  
#dff = prioridad.comportamiento_compra(ruta, hoja)   
#print(dff)

os.startfile(ruta) """
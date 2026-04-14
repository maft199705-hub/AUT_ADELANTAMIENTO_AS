import pandas as pd
import numpy as np
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
from logica_frecuencias import logica_frecuencias
from logica_prioridad import logica_prioridad

class r_principal: 
    funcion = funciones()
    log_frecuencias = logica_frecuencias()
    log_prioridad = logica_prioridad()
    
    def __init__(self):
        pass
    
#---------------------------------------FUNCIONES---------------------------------------#
#---------------------------    GENERICAS
#---------------------------    ESPECIFICAS   
    def DIAS_DE_LLAMADO(self, dff, ruta, hoja): #REALIZA EL CALCULO DE LOS DIAS DE LLAMADO PREVIA, INSITU Y POST 
        try:
            #OJO DIAS DE LLAMADO Y PRIORIZACION DEBE DE TENER EXACTAMENTE LOS MISMOS CLIENTES
            #LOGICA DE CALCULO DE DIAS DE LLAMADO PREVIA, INSITU Y POST-------------------------
            df = self.funcion.leer(ruta, hoja[0]) #hoja[0] lee 'DIAS DE LLAMADO'
           
            df['dias_llamado_num'] = df['dias_llamado'].str.upper().apply(self.funcion.letra_to_numero) #se normaliza a mayusculas y se convierte a numero
            df['dias_despacho_num'] = df['dias_despacho'].str.upper().apply(self.funcion.letra_to_numero)
            df['feriados_num'] = df['dias_feriados'].str.upper().apply(self.funcion.letra_to_numero)
            df['regla_num'] = df['regla_despachos'].apply(self.funcion.regla_to_num)

            res= df.apply(self.log_frecuencias.calculo_llamado_post, axis=1) #calculo de dias de llamado post
            df[['dias_llamado_post_num', 'dias_llamado_insitu_post_num']] = pd.DataFrame(res.tolist(), index=df.index)
            
            res= df.apply(self.log_frecuencias.calculo_llamado_insitu, axis=1) #calculo de dias de llamado insitu
            df[['dias_llamado_insitu_num', 'dias_despacho_insitu_num', 'dias_llamado_previa_insitu_num']] = pd.DataFrame(res.tolist(), index=df.index)
            
            res= df.apply(self.log_frecuencias.calculo_llamado_previa, axis=1) #calculo de dias de llamado previa
            df['dias_llamado_previa_num'] = res
            
            df['dias_llamado_previa'] = df['dias_llamado_previa_num'].apply(self.funcion.numero_to_letra)
            df['dias_llamado_insitu'] = df['dias_llamado_insitu_num'].apply(self.funcion.numero_to_letra)
            df['dias_despacho_insitu'] = df['dias_despacho_insitu_num'].apply(self.funcion.numero_to_letra)
            df['dias_llamado_post'] = df['dias_llamado_post_num'].apply(self.funcion.numero_to_letra)
            df['prioridad'] = dff['prioridad']
        
            del df['dias_llamado_num']
            del df['dias_despacho_num']
            del df['feriados_num'] 
            del df['dias_llamado_insitu_post_num']   
            del df['regla_num']
            del df['dias_llamado_previa_insitu_num']
            del df['dias_llamado_previa_num']
            del df['dias_llamado_insitu_num']
            del df['dias_despacho_insitu_num']
            del df['dias_llamado_post_num']
            
            self.funcion.escribir( df, ruta, hoja[0])   
            return 0

        except Exception as e:
            print(f'Error: {e} /ERROR CLASS R_PRINCIPAL: DIAS_DE_LLAMADO()')
            return None
        
    def DATOS_PRIORIZACION(self, ruta, hoja): #REALIZA EL CALCULO DE LOS DATOS DE PRIORIZACION Y EL INDICE DE PRIORIDAD PARA LOS CLIENTES
        try:
            
            self.log_prioridad.descartes(ruta, hoja)
            self.log_prioridad.netos_kilos_ultimo(ruta, hoja) 
            self.log_prioridad.contactabilidad_efectividad(ruta, hoja)  
            dff = self.log_prioridad.comportamiento_compra(ruta, hoja) 
            
            #calculo final de priorizacion
            dff ['prioridad'] = dff ['comportamiento de compra'] + dff ['kilos'] + dff ['netos'] + dff ['talla']+ dff ['contactabilidad'] + dff ['efectividad'] 
            dff.loc[(dff['nuevo'] == 1) | (dff['bloqueado'] == 1) | (dff['cerrado'] == 1), 'prioridad'] = 0 # anulacion por descartes
            
            col = dff.pop('prioridad')     # saca la columna
            dff.insert(10, 'prioridad', col)  # la inserta en la posición deseada
            
            self.funcion.escribir(dff, ruta, hoja[1])
            
            return dff
            
        except Exception as e:
            print(f'Error: {e} /ERROR CLASS R_PRINCIPAL: DATOS_PRIORIZACION()')
            return None

#--------------------------------------  EJECUCION  ---------------------------------# 

""" ruta = 'C:/Users/moise/Desktop/MY PROYECTS/AUT_ADELANTAMIENTO/adelantamiento.xlsx' #resporte[r'reporte principal', r'reporte 2', r'reporte 3']
hoja =['DIAS DE LLAMADO', 'DATOS PRIORIZACION', 'RESUMEN DE PEDIDOS', 'RESUMEN DE DESCARTES', 'RESUMEN DE CONTAC Y EFECT']


ejecutar = r_principal()

archivo1 = ejecutar.DATOS_PRIORIZACION(ruta, hoja) 
#archivo2= ejecutar.DIAS_DE_LLAMADO(ruta, hoja)


ruta = os.startfile(ruta)
 """




        
        




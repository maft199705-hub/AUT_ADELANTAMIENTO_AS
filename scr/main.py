import os
import  sys
from datetime import date
from r_principal import r_principal

class main:
    r_principal = r_principal()
    
    def __init__(self):
        pass
      
    

#--------------------------------------  EJECUCION  ---------------------------------#     
try:
    if __name__ == "__main__":
        
        hoy = date.today()
        cierre = date(2026, 4, 30)
      
        if hoy > cierre :
            print(f'LICENCIA DE USO CADUCADA / VENCIMIENTO {cierre}' )
            input('Presione ENTER PARA CONTINUAR')
            sys.exit(1)
            
        
        print('PROGRAMA AUT_ADELANTAMIENTO INICIALIZADO...')
        
        ruta = input("Ingrese ruta del archivo a trabajar adelantamiento.xls: ").strip().strip('"')
        
        print(f'PROCESANDO ARCHIVO {ruta}')
        
        hoja =['DIAS DE LLAMADO', 'DATOS PRIORIZACION', 'RESUMEN DE PEDIDOS', 'RESUMEN DE DESCARTES', 'RESUMEN DE CONTAC Y EFECT']

        iniciar = main()
        
        dff = iniciar.r_principal.DATOS_PRIORIZACION(ruta, hoja)
        iniciar.r_principal.DIAS_DE_LLAMADO(dff, ruta, hoja)

        os.startfile(ruta) 
    
except Exception as e:
    print(f'Error en ejecucion del programa AUT_ADELANTAMIENTO: {e}' )
    input('Presione ENTER PARA CONTINUAR')
    sys.exit(1)
    

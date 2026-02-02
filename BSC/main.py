
from opciones import opciones_principales_func
from pipeline_grupos_economicos import pipeline_ge_func
from pipeline_txt_deudores import generate_txt_func

#from utils.paths import definir_ruta_func
#print("BASE (exe):", definir_ruta_func())

#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------

while True:

    eleccion= opciones_principales_func()
    
    if eleccion== "1":
        
        generate_txt_func()
        
    elif eleccion== "2":
        
        pipeline_ge_func()
    
    elif eleccion== "3":
        
        pipeline_ge_func()

    elif eleccion== "4":
        
        print("\nProceso terminado...")
        
        input("\nPresione 'enter' para salir")
        
        break
     
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------


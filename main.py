
from opciones import opciones_principales_func
from importar_inputs import (importar_deudores_func, importar_input_manual, importar_sp_func, TC_Sdo_No_Usado_Func)
from importar.deposito_acuerdos import Deposito_Acuerdos_Func
from utils.paths import definir_ruta_func
from utils.validaciones import validar_archivos_existen
from grupos_economicos import (crear_tabla_maestro_grupos, alta_clientes_func, baja_clientes_func, exportar_maestro_func, 
                               importar_base_func, mostrar_tabla_func)
from opciones import opciones_ge


#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------

eleccion= opciones_principales_func()

if eleccion== "1":
    
    fec_def= validar_archivos_existen()
    
    ruta_bases= definir_ruta_func()
    
    importar_deudores_func(ruta_bases, fec_def)
    
    Input_Manual= importar_input_manual(ruta_bases, fec_def)
    
    SP, lim_TC_SP= importar_sp_func(ruta_bases, fec_def)
    
    TC_Sdo_No_Usado= TC_Sdo_No_Usado_Func(fec_def)
    
    Deposito_Acuerdos_Func(ruta_bases, fec_def)
    
elif eleccion== "2":
    
    crear_tabla_maestro_grupos()
    
    eleccion= opciones_ge()
    
    if eleccion== "1":
        alta_clientes_func()
    elif eleccion== "2":
        baja_clientes_func()
    elif eleccion== "3":
        exportar_maestro_func()
    elif eleccion== "4":
        importar_base_func()
    elif eleccion== "5":
        mostrar_tabla_func()
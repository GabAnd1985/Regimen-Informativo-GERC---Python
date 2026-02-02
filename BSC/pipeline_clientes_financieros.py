
from clientes_financieros import (crear_tabla_clientes_financieros, alta_clientes_fcieros_func, baja_clientes_fcieros_func,
                                  exportar_maestro_fcieros_func, importar_base_fcieros_func, mostrar_tabla_fcieros_func)
from opciones import opciones_ge

#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------


def pipeline_ge_func():
    
    while True:
    
        crear_tabla_clientes_financieros()
        
        eleccion= opciones_ge()
        
        if eleccion== "1":
            alta_clientes_fcieros_func()
        elif eleccion== "2":
            baja_clientes_fcieros_func()
        elif eleccion== "3":
            exportar_maestro_fcieros_func()
        elif eleccion== "4":
            importar_base_fcieros_func()
        elif eleccion== "5":
            mostrar_tabla_fcieros_func()        
        elif eleccion== "6":
            break
        
    return
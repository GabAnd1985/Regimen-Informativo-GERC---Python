
from grupos_economicos import (crear_tabla_maestro_grupos, alta_clientes_func, baja_clientes_func, exportar_maestro_func, 
                               importar_base_func, mostrar_tabla_func)
from opciones import opciones_ge

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------


def pipeline_ge_func():

    while True:    

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
        elif eleccion== "6":
            break
        
    return


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

from utils.validaciones import selector


#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------


def opciones_principales_func():

    opciones= """\nConsidere las siguientes opciones: 
                
                1) Correr GERC - Generar txt.
                2) Administrar maestro de Grupos Económicos.
                3) Administrar maestro de Clientes Financieros.
                4) Salir.
                """
    
    print(opciones)
    
    eleccion= selector("Ingrese la opción que desea", 1, 4)

    return eleccion


#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------


def opciones_ge():

    opciones= """\nConsidere las siguientes opciones: 
                
                1) Dar de alta clientes.
                2) Dar de baja clientes.
                3) Exportar maestro.
                4) importar un excel.
                5) Ver la tabla.
                6) Volver al menú anterior.
                """
    
    print(opciones)
    
    eleccion= selector("Ingrese la opción que desea", 1, 6)
    
    return eleccion
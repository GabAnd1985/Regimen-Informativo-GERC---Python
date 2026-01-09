
import glob
from utils.paths import definir_ruta_func


#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------


def validar_fecha_func(fec):

    """valida que el valor ingresado tenga 7 dígitos, que el segundo sea punto, 
       que os dos primeros y los 4 últimos sean números y que los dos primeros
       no sean menores a 1 ni mayores a 12""" 

    if len(fec)!= 7:
        return False
    
    elif fec[2]!= ".":
        return False
    
    elif fec[0:2].isdigit()== False:
        return False
    
    elif fec[3:7].isdigit()== False:
        return False
        
    elif (int(fec[0:2]) > 12 or int(fec[0:2]) < 1):
        return False
    
    else:
        return True


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------


def pedir_fecha_func():

    """Solicita la fecha al usuario, corre la función que la valida, se fija
       que haya un archivo con esa fechas sino vuelve a solicitarla"""    

    Fecha= input("\npor favor ingrese la fecha a trabajar (mm.yyyy): ")    

    res_fec= validar_fecha_func(Fecha)    

    if res_fec== True:
        return Fecha

    while res_fec== False:

        print("\nFormato inválido, por favor vuelva a intentarlo.")        

        Fecha= input("\npor favor ingrese la fecha a trabajar (mm.yyyy): ")    
    
        res_fec= validar_fecha_func(Fecha)
        
        if res_fec== True:
            return Fecha


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------


def validar_archivos_existen():

    ruta_bases= definir_ruta_func()
    
    while True:
    
        fec_def= pedir_fecha_func()
        
        #-------------------------------------------------------------------------
        
        path_deudores= "{}/Inputs/Deudores".format(ruta_bases)
        
        filelist_deudores= glob.glob("{}/*.txt".format(path_deudores)) 
        
        newlist_deudores= []
        
        for file in filelist_deudores:
            newlist_deudores.append(file[(len(path_deudores) + 1):(len(path_deudores) + len("DEUDORES mm.yyyy") + 1)])
        
        #-------------------------------------------------------------------------
            
        path_manuales= "{}/Inputs/Inputs Manuales".format(ruta_bases)
        
        filelist_manuales= glob.glob("{}/*.xlsx".format(path_manuales)) 
        
        newlist_manuales= []
        
        for file in filelist_manuales:
            newlist_manuales.append(file[(len(path_manuales) + 1):(len(path_manuales) + len("Input Manual mm.yyyy") + 1)])
        
        #-------------------------------------------------------------------------
        
        path_sp= "{}/Inputs/Sector Público".format(ruta_bases)
        
        filelist_sp= glob.glob("{}/*.xlsx".format(path_sp)) 
        
        newlist_sp= []
        
        for file in filelist_sp:
            newlist_sp.append(file[(len(path_sp) + 1):(len(path_sp) + len("Sector Público mm.yyyy") + 1)])
    
        #-------------------------------------------------------------------------
        
        control_a= "DEUDORES {}".format(fec_def)
        
        control_b= "Inputs Manual {}".format(fec_def)
        
        control_c= "Sector Público {}".format(fec_def)
        
        if control_a not in newlist_deudores:
            print("\nNo existe el archivo DEUDORES {}".format(fec_def))
            continue
        if control_b not in newlist_manuales:
            print("\nNo existe el archivo Input Manual {}".format(fec_def))
            continue
        if control_c not in newlist_sp:
            print("\nNo existe el archivo Sector Público {}".format(fec_def))
            continue
        
        break

    return fec_def

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------


def validar_numero(opcion):
    """sirve para validar que la opción ingresada sea un número"""
    
    if opcion.isdigit()== False:
        return False
    else:
        return True


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------


def selector_num(texto):

    while True:
        
        op_1= input("\n{}: ".format(texto))
        
        resp= validar_numero(op_1)
        
        if resp== True:
            break
        
        print("\nel valor ingresado no es válido...")
        
    return op_1


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------


def validar_opcion_func(opcion, min_op, max_op):
    """Sirve para validar la opción ingresada por un usuario 
       de un menú de opciones"""
    
    if opcion.isdigit()== False:
        return False
    elif int(opcion) < min_op:
        return False
    elif int(opcion) > max_op:
        return False
    else:
        return True
    

#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------

def selector(texto, min_op, max_op):

    while True:
        
        op_1= input("\n{}: ".format(texto))
        
        resp= validar_opcion_func(op_1, min_op, max_op)
        
        if resp== True:
            break
        
        print("\nOpción inválida...")
        
    return op_1


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------


def validacion_si_no(texto):

    continua= input("\n{} (s/n)? ".format(texto))
    
    while continua not in ["n", "N", "s", "S"]:
        print("\nEl valor ingresado no es correcto")
        
        continua= input("\n{} (s/n)? ".format(texto))        
        
    return continua


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
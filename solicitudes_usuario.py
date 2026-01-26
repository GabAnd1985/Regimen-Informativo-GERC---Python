
from utils.validaciones import selector_num
from utils.validaciones import validar_fecha_func
import glob
from utils.paths import definir_ruta_func


#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------


def solicitud_Cn1_func():

    texto= "Por favor ingrese el Cn1 del mes correspondiente (M$)"
    
    Cn1= selector_num(texto)

    return Cn1


#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------


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
        
        control_b= "Input Manual {}".format(fec_def)
        
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


#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------


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


#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------


if __name__ == "__main__":
    main()
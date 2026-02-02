
import pandas as pd
from utils.paths import definir_ruta_func
from solicitudes_usuario import validar_archivos_existen
from importar.parsear_deudores import Reserva_SQL_Func


#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------


def importar_deudores_func(path, fec):
    
    path_inputs_deudores= path / "Inputs" / "Deudores"

    path_bases_deudores= path / "Bases" / "Deudores"
    
    name= list(range(29))
                    
    df= pd.read_table("{}/DEUDORES {}.txt".format(path_inputs_deudores, fec), names= name , sep= ";", encoding='latin-1',
                                  dtype={3: str}) 
    
    Reserva_SQL_Func(df, path_bases_deudores, fec)

    return 


#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------


def importar_input_manual(path, fec):

    path_manual= path / "Inputs" / "Inputs Manuales"
    
    xlsx= pd.ExcelFile("{}/Input Manual {}.xlsx".format(path_manual, fec)) 
    
    Input_Manual= pd.read_excel(xlsx)
    
    return Input_Manual


#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------


def importar_sp_func(path, fec):

    path_SP= path / "Inputs" / "Sector Público"
    
    SP= pd.read_excel("{}/Sector Público {}.xlsx".format(path_SP, fec), "Asistencias") 
    
    lim_TC_SP= pd.read_excel("{}/Sector Público {}.xlsx".format(path_SP, fec), "Lim No Util Tarjetas")

    return SP, lim_TC_SP


#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------


def importar_RD_MP_func(path, fec):

    path_manual= path / "Inputs" / "RD_MP"
    
    RD_MP_1= pd.read_table("{}/RD_MP {}.txt".format(path_manual, fec), sep= ";", header= None)
    
    RD_MP_2= RD_MP_1[[0, 1, 7]]
    
    RD_MP= RD_MP_2.rename(columns={0: 'NroSFB', 1: 'NOMBRE', 7: 'CUIT'})
    
    return RD_MP


#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------


def main():

    fec_def= validar_archivos_existen()
    
    ruta_bases= definir_ruta_func()
    
    importar_deudores_func(ruta_bases, fec_def)
    
    Input_Manual= importar_input_manual(ruta_bases, fec_def)
    
    RD_MP= importar_RD_MP_func(ruta_bases, fec_def)
    
    SP, lim_TC_SP= importar_sp_func(ruta_bases, fec_def)
    
    return Input_Manual, RD_MP


#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------


if __name__ == "__main__":
    main()



































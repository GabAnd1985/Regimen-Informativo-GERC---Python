
import pandas as pd
from utils.paths import definir_ruta_func
from utils.validaciones import validar_archivos_existen
from importar.parsear_deudores import Reserva_SQL_Func
import pyreadstat
import sys
import numpy as np


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
    
    fec_format= fec[3:7] + fec[0:2]
    
    Reserva_SQL_Func(df, path_bases_deudores, fec_format)

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


def TC_Sdo_No_Usado_Func(fec):

    Ruta_SAS= "//172.30.10.43/sas_bsc/Data/NIIF9 BSC/Test/PCE/FL/PE/Resultados"
    
    fec_1= fec[3:7] + fec[0:2]
    
    try:
    
        TC_1, _ = pyreadstat.read_sas7bdat("{}/PE_{}.sas7bdat".format(Ruta_SAS, fec_1))   
    
    except:
        
        print("\nEl archivo PR_{} no existe.")
    
        print("\nSe cierra el aplicativo.")
    
        input("\nPresione 'Enter' para salir...")    
    
        sys.exit()
    
    TC_2= TC_1[["id_cliente", "id_operacion_mes", "producto_mes", "agrup_1", "agrup_0", "sal_total", "limite"]]
    
    TC_3= TC_2[TC_2["agrup_1"]== "Tarjeta de Crédito"]
    
    TC_4a= TC_3[TC_3["agrup_0"]!= "TC cumplimiento Irregular"]
    
    TC_4= TC_4a.copy()
    
    TC_4["id_cliente"]= TC_4["id_cliente"].astype("int64")
    
    TC_5a= TC_4[TC_4["limite"] > 0]
    
    TC_5= TC_5a.copy()
    
    TC_5["TC_Incorporar_1"]= TC_5["limite"] - TC_5["sal_total"]
    
    TC_5["TC_Incorporar_1"]= np.where(TC_5["TC_Incorporar_1"] < 0, 0, TC_5["TC_Incorporar_1"])
    
    TC_5["TC_Incorporar"]= TC_5["TC_Incorporar_1"] * 0.1
    
    grouped= TC_5["TC_Incorporar"].groupby(TC_5["id_cliente"])
    
    TC_6= grouped.sum()
    
    TC_Sdo_No_Usado= TC_6.reset_index()

    return TC_Sdo_No_Usado


#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------


def main():

    fec_def= validar_archivos_existen()
    
    ruta_bases= definir_ruta_func()
    
    importar_deudores_func(ruta_bases, fec_def)
    
    Input_Manual= importar_input_manual(ruta_bases, fec_def)
    
    SP, lim_TC_SP= importar_sp_func(ruta_bases, fec_def)
    
    TC_Sdo_No_Usado= TC_Sdo_No_Usado_Func(fec_def)
    
    return Input_Manual, TC_Sdo_No_Usado


#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------


if __name__ == "__main__":
    main()



































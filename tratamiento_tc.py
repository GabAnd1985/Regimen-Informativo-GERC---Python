
from solicitudes_usuario import validar_archivos_existen
import pyreadstat
import numpy as np
from config.config_local import Ruta_SAS


#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------


def armado_tc_func(fec, Ruta_SAS):

    fec_1= fec[3:7] + fec[0:2]
    
    TC_1, _ = pyreadstat.read_sas7bdat("{}/PE_{}.sas7bdat".format(Ruta_SAS, fec_1))
    
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
    
    TC_Incorporar= TC_6.reset_index()

    return TC_Incorporar


#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------


def main():
    
    fec_def= validar_archivos_existen()
    
    TC_Incorporar= armado_tc_func(fec_def, Ruta_SAS)
    
    return TC_Incorporar


#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
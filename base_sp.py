
import pandas as pd
import numpy as np
from solicitudes_usuario import solicitud_Cn1_func
from utils.paths import definir_ruta_func
from solicitudes_usuario import validar_archivos_existen
import sqlite3
from importar_inputs import importar_sp_func


#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------


def deuda_tc_sp(path, fec):

    fec_1= fec[3:7] + fec[0:2] 
    
    db= sqlite3.connect("{}/Bases/Deudores/Deudores_{}.db".format(path, fec_1))
    
    df_4305= pd.read_sql_query("SELECT * from d4305", db)
    
    df_4306= pd.read_sql_query("SELECT * from d4306", db)
    
    db.close()
    
    #------------------------------------------------------------------------
    
    df_1= df_4305.copy()
    
    df_1["Cond"]= df_1["Residencia"].isin([3, 4])
    
    df_2= df_1[df_1["Cond"]== True]
    
    df_3= df_2[["CUIT", "Denominación"]]
    
    #------------------------------------------------------------------------
    
    df_4= df_4306.copy()
    
    df_5= df_4[df_4["Tipo Asistencia"]== "10"]
    
    df_6a= df_5[["CUIT", "Gtias Pref A Capital Total", "Gtias Pref B Capital Total", "Gtias Pref B Intereses Total",
                "Sin Gtias Pref Cap Total", "Sin Gtia Pref Interes Total"]]
    
    df_6= df_6a.copy()
    
    df_6["Gtias Pref B Intereses Total"]= df_6["Gtias Pref B Intereses Total"].astype('float64') 
    
    df_6["Sin Gtia Pref Interes Total"]= df_6["Sin Gtia Pref Interes Total"].astype('float64')
    
    df_7= df_6.fillna(0)
    
    df_7["Deuda_Total"]= (df_7["Gtias Pref A Capital Total"] + df_7["Gtias Pref B Capital Total"] + df_7["Gtias Pref B Intereses Total"] + 
                          df_7["Sin Gtias Pref Cap Total"] + df_7["Sin Gtia Pref Interes Total"])
    
    df_8= df_7[["CUIT", "Deuda_Total"]]
    
    #------------------------------------------------------------------------
    
    Deuda_TC_SP_1= pd.merge(df_3, df_8, on= "CUIT", how= "left")
    
    Deuda_TC_SP= Deuda_TC_SP_1.fillna(0)

    return Deuda_TC_SP


#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------


def base_sp_func(lim_TC_SP, Deuda_TC_SP, SP):

    lim_TC_2= lim_TC_SP[lim_TC_SP["Limite"]!= 0]
    
    lim_TC_3= pd.merge(lim_TC_2, Deuda_TC_SP, on= "CUIT", how= "left")
    
    lim_TC_4= lim_TC_3.drop(["Denominación"], axis= "columns")
    
    lim_TC_4["Deuda_Total"]= lim_TC_4["Deuda_Total"].fillna(0)
    
    lim_TC_4["SDO_NO_UTIL_1"]= lim_TC_4["Limite"] - (lim_TC_4["Deuda_Total"] * 1000)
    
    lim_TC_4["SDO_NO_UTIL"]= (lim_TC_4["SDO_NO_UTIL_1"] * 0.1) / 1000
    
    lim_TC_5= lim_TC_4.drop(["Limite", "Deuda_Total", "SDO_NO_UTIL_1"], axis= "columns")
    
    lim_TC_5["EXPOSICIÓN BRUTA"]= lim_TC_5["SDO_NO_UTIL"] 
    
    lim_TC_5["EXPOSICIÓN NETA DE CRC"]= lim_TC_5["SDO_NO_UTIL"] 
    
    lim_TC_5["EXPOSICIÓN NETA DE GTIAS A Y B"]= lim_TC_5["SDO_NO_UTIL"] 
    
    lim_TC_6= lim_TC_5.drop(["SFB", "SDO_NO_UTIL"], axis= "columns")
    
    lim_TC_def= lim_TC_6.rename(columns={'Denominacion': 'DENOMINACION'})
    
    #--------------------------------------------------------------------
    
    SP_2= SP[["TIPO ID", "CUIT", "DENOMINACION", "EXPOSICIÓN BRUTA", "EXPOSICIÓN NETA DE CRC", "EXPOSICIÓN NETA DE GTIAS A Y B"]]
    
    SP_3= pd.concat([SP_2, lim_TC_def], axis= 0)
    
    SP_4= SP_3.groupby(['TIPO ID'])[['EXPOSICIÓN BRUTA', 'EXPOSICIÓN NETA DE CRC', "EXPOSICIÓN NETA DE GTIAS A Y B"]].sum().reset_index()
    
    SP_4["CODIGO"]= ""
    
    SP_4["DENOMINACION"]= ""
    
    SP_4["NIVEL CONSOLID"]= 0
    
    Cn1= int(solicitud_Cn1_func())
    
    SP_4["TIPO DE EXPOSICIÓN"]= np.where(SP_4['EXPOSICIÓN BRUTA'] > (0.1 * Cn1), 2, 3)
    
    Base_SP_def= SP_4[["TIPO ID", "CODIGO", "DENOMINACION", "NIVEL CONSOLID", 
                     'EXPOSICIÓN BRUTA', 'EXPOSICIÓN NETA DE CRC', 
                     "EXPOSICIÓN NETA DE GTIAS A Y B", "TIPO DE EXPOSICIÓN"]]
    
    Base_SP_def['TIPO ID']= Base_SP_def['TIPO ID'].astype('int64')
    
    return Base_SP_def


#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------

def main():

    fec_def= validar_archivos_existen()
    
    ruta_bases= definir_ruta_func()
    
    SP, lim_TC_SP= importar_sp_func(ruta_bases, fec_def)
    
    Deuda_TC_SP= deuda_tc_sp(ruta_bases, fec_def)
    
    Base_SP_def= base_sp_func(lim_TC_SP, Deuda_TC_SP, SP)
    
    return Base_SP_def


#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------


if __name__ == "__main__":
    main()
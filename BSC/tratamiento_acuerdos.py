
from utils.paths import definir_ruta_func
from solicitudes_usuario import validar_archivos_existen
import sqlite3
import pandas as pd
import numpy as np
from importar_inputs import importar_RD_MP_func


#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------


def armado_acuerdos_func(path, fec, RD_MP):

    fec_1= fec[3:7] + fec[0:2]
    
    db= sqlite3.connect("{}/Bases/Acuerdos/ACMAC_{}.db".format(path, fec_1))
    
    Acc_1= pd.read_sql_query("SELECT * from ACMAC", db)
    
    db.close()
    
    #Ajusto la fecha de vencimiento de los acuerdos al formato requerido
    
    Acc_1["Vto_Acuerdo_v1"]= np.where(Acc_1["Vto_Acuerdo"] < 100000, "0" + Acc_1["Vto_Acuerdo"].astype(str), Acc_1["Vto_Acuerdo"].astype(str)) 
    
    Acc_2a= Acc_1[Acc_1["Vto_Acuerdo_v1"]!= "00"]
    
    Acc_2= Acc_2a.copy()
    
    Acc_2["Vto_Acuerdo_v2"]= pd.to_datetime(Acc_2["Vto_Acuerdo_v1"], format='%d%m%y') 
    
    Acc_2["Vto_Acuerdo_v3"]= Acc_2["Vto_Acuerdo_v2"].dt.date
    
    Acc_2["Fecha_Ref"]= Acc_2["Vto_Acuerdo_v3"].astype(str).str[0:4] + Acc_2["Vto_Acuerdo_v3"].astype(str).str[5:7]
    
    Acc_2["Fecha_Ref"]= Acc_2["Fecha_Ref"].astype(int)
    
    Acc_3= Acc_2[Acc_2["Fecha_Ref"] > int(fec_1)]
    
    Acc_4= Acc_3[Acc_3["Estado"]== 2]
    
    Acc_5= Acc_4[Acc_4["Tipo"]!= 99]
    
    Acc_6= Acc_5[Acc_5["Monto_Acuerdo"] != 0]
    
    Acc_7= Acc_6[Acc_6["Moneda"]== 80]
    
    grouped= Acc_7["Monto_Acuerdo"].groupby([Acc_7["NroSFB"]])
    
    Acc_8= grouped.sum()
    
    Acc_9= Acc_8.reset_index()
    
    #--------------------------------------------------------------------------------
    
    #Extraemos del diseño 4306 la deuda en adelantos "01"
    
    db= sqlite3.connect("{}/Bases/Deudores/Deudores_{}.db".format(path, fec_1))
    
    df_4306= pd.read_sql_query("SELECT * from d4306", db)
    
    db.close()
    
    df_01= df_4306[df_4306["Tipo Asistencia"]== "01"]
    
    df_02= df_01[["CUIT", "Gtias Pref A Capital Total", "Gtias Pref B Capital Total", "Gtias Pref B Intereses Total", "Sin Gtias Pref Cap Total", "Sin Gtia Pref Interes Total"]]
    
    cols= ["Gtias Pref A Capital Total", "Gtias Pref B Capital Total", "Gtias Pref B Intereses Total", "Sin Gtias Pref Cap Total", "Sin Gtia Pref Interes Total"]
    
    df_03= df_02.copy()
        
    df_03[cols]= df_03[cols].astype(float).fillna(0)
    
    df_03["Total_Acuerdos"]= (df_03["Gtias Pref A Capital Total"] + df_03["Gtias Pref B Capital Total"]
                             + df_03["Gtias Pref B Intereses Total"] + df_03["Sin Gtias Pref Cap Total"]
                             + df_03["Sin Gtia Pref Interes Total"])
    
    df_04= df_03[["CUIT", "Total_Acuerdos"]]
    
    #--------------------------------------------------------------------------------
    
    Acc_10= pd.merge(Acc_9, RD_MP, left_on= ["NroSFB"], right_on= ["NroSFB"], how= "left")
    
    #Cruzamos ambas tablas generadas
    
    Acc_11= pd.merge(Acc_10, df_04, left_on= ["CUIT"], right_on= ["CUIT"], how= "left")
    
    Acc_11["Total_Acuerdos"]= Acc_11["Total_Acuerdos"].fillna(0) 
    
    Acc_11["Total_Acuerdos"]= Acc_11["Total_Acuerdos"] * 1000
    
    Acc_11["Saldo acuerdo no utilizado"]= Acc_11["Monto_Acuerdo"] - Acc_11["Total_Acuerdos"]
    
    Acc_12= Acc_11[["CUIT", "Saldo acuerdo no utilizado"]]
    
    #--------------------------------------------------------------------------------
    
    grouped= Acc_12["Saldo acuerdo no utilizado"].groupby(Acc_12["CUIT"])
    
    Acc_13= grouped.sum()
    
    Acc_14= Acc_13.reset_index()
    
    Acc_14["Saldo acuerdo no utilizado"]= np.where(Acc_14["Saldo acuerdo no utilizado"] < 0, 0, Acc_14["Saldo acuerdo no utilizado"])
    
    Acc_14["Acc_Incorporar"]= Acc_14["Saldo acuerdo no utilizado"] * 0.1
    
    #-------------------------------------------------------------------
    
    Acc_Incorporar= Acc_14[["CUIT", "Acc_Incorporar"]]

    return Acc_Incorporar


#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------


def main():
    
    fec_def= validar_archivos_existen()

    ruta_bases= definir_ruta_func()

    RD_MP= importar_RD_MP_func(ruta_bases, fec_def)

    Acc_Incorporar= armado_acuerdos_func(ruta_bases, fec_def, RD_MP)
    
    return Acc_Incorporar


#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------


if __name__ == "__main__":
    main()

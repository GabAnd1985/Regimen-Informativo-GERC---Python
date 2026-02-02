
import pandas as pd
import numpy as np
import sqlite3


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


def armado_BSF(ruta_bases, Base_Completa, df_Individual_SV, fec_def):

    db= sqlite3.connect("{}/Bases/Maestros/maestro_grupos.db".format(ruta_bases))
    
    Maestro_1= pd.read_sql_query("SELECT * from maestro_grupos", db)
    
    db.close()
    
    Maestro_1a= Maestro_1[["cuit", "denominacion", "codigo_grupo", "orden"]]
    
    Maestro= Maestro_1a.rename(columns={'cuit': 'CUIT', 'denominacion': 'DENOMINACION', 'codigo_grupo': 'CODIGO', 'orden': 'ORDEN'})
    
    BC_1A= Base_Completa[Base_Completa["TIPO ID"]!= "88"]
    
    BC_1= BC_1A.drop(["TIPO DE EXPOSICIÓN"], axis= "columns")
    
    #---------------------------------------------------------
    
    BC_2= pd.merge(Maestro, df_Individual_SV, on= "CUIT", how= "left")
    
    BC_3= BC_2[["CUIT", "DENOMINACION", "EXPOSICIÓN BRUTA", "EXPOSICIÓN NETA DE CRC", "EXPOSICIÓN NETA DE GTIAS A Y B"]]
    
    BC_4= BC_3.fillna(0)
    
    BC_4["TIPO ID"]= "11"
    
    BC_4["NIVEL CONSOLID"]= "0"
    
    BC_5= BC_4.rename(columns={'CUIT': 'CODIGO'})
    
    #---------------------------------------------------------
    
    BC_6= pd.concat([BC_1, BC_5], axis= 0) 
    
    BC_6["TIPO ID"]= BC_6["TIPO ID"].astype(int) 
    
    conditions= [((BC_6["TIPO ID"] == 10)),
                 ((BC_6["TIPO ID"] == 20)),
                 ((BC_6["TIPO ID"] == 30)),
                 ((BC_6["TIPO ID"] == 11)),
                 ((BC_6["TIPO ID"] == 89))]
    
    values= [3, 3, 3, 1, 1]
    
    BC_6['SECTOR CLIENTE'] = np.select(conditions, values)
    
    #---------------------------------------------------------
    
    fec_1= fec_def[3:7] + fec_def[0:2] 
    
    db= sqlite3.connect("{}/Bases/Deudores/Deudores_{}.db".format(ruta_bases, fec_1))
    
    df_4305= pd.read_sql_query("SELECT * from d4305", db)
    
    db.close()
    
    df_1= df_4305[df_4305["Residencia"]== 2]
    
    df_2= df_1[["CUIT"]]
    
    df_3= df_2.drop_duplicates()
    
    #---------------------------------------------------------
    
    xlsx= pd.ExcelFile("{}/Inputs/Maestros/Maestro_Financiero.xlsx".format(ruta_bases))
    
    Maestro_Fin_1= pd.read_excel(xlsx)
    
    xlsx.close()
    
    Maestro_Fin= Maestro_Fin_1[["CODIGO", "DENOMINACION", "SECTOR"]]
    
    #---------------------------------------------------------
    
    Control_1= pd.merge(df_3, Maestro_Fin, left_on= "CUIT", right_on= "CODIGO", how= "left")
    
    Control_2= Control_1[Control_1["CODIGO"].isnull()]
    
    Control_Maestro_Financiero= Control_2[["CUIT"]]
    
    Control_Maestro_Financiero["Acción"]= "Agregar en el Maestro Financiero"
    
    #---------------------------------------------------------
    
    BC_7= pd.merge(BC_6, Maestro_Fin, on= "CODIGO", how= "left")
    
    BC_8= BC_7.drop(["DENOMINACION_y"], axis= "columns")
    
    BC_9= BC_8.rename(columns={'DENOMINACION_x': 'DENOMINACION'})
    
    BC_9["SECTOR CLIENTE"]= np.where(~BC_9["SECTOR"].isnull(), BC_9["SECTOR"], BC_7["SECTOR CLIENTE"])
    
    Base_BSF= BC_9.drop(["SECTOR"], axis= "columns")

    return Control_Maestro_Financiero, Base_BSF


#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#---------------------------------------------------------------------
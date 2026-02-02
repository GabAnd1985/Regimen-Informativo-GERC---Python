

import sqlite3
import pandas as pd


#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------


def armado_sin_sp_func(df_Individual_SV, path):

    db= sqlite3.connect("{}/Bases/Maestros/maestro_grupos.db".format(path))
    
    Maestro_1= pd.read_sql_query("SELECT * from maestro_grupos", db)
    
    db.close()
    
    #----------------------------------------------------------------
    
    #Generamos el total por grupo
    
    Maestro= Maestro_1[["cuit", "codigo_grupo", "orden"]]
    
    df_1= pd.merge(df_Individual_SV, Maestro, left_on= "CUIT", right_on= "cuit", how= "left")
        
    df_2= df_1.fillna(0)
    
    g_1= df_2[df_2["codigo_grupo"]!= 0]
    
    grouped= g_1[["EXPOSICIÓN BRUTA", "EXPOSICIÓN NETA DE CRC", "EXPOSICIÓN NETA DE GTIAS A Y B"]].groupby([g_1["codigo_grupo"]])
    
    g_2= grouped.sum()
    
    g_3= g_2.reset_index(level=["codigo_grupo"])
    
    g_5= Maestro[Maestro["orden"]== 1]
    
    g_6= pd.merge(g_5, g_3, on= "codigo_grupo", how= "left")
    
    g_7= g_6.dropna()
    
    g_8a= g_7.drop(["orden", "cuit"], axis= "columns")
    
    g_8= g_8a.rename(columns={'codigo_grupo': 'CODIGO'})
    
    g_8["TIPO ID"]= "88"
    
    #----------------------------------------------------------------
    
    #Para los que no son grupos, armamos el total individual
    
    ng_1= df_2[df_2["codigo_grupo"]== 0]
    
    ng_2= ng_1.drop(["codigo_grupo", "orden", "cuit"], axis= "columns")
    
    ng_2["TIPO ID"]= "11"
    
    ng_3= ng_2.rename(columns= {"Denominación": "DENOMINACION", "CUIT": "CODIGO"})
    
    #----------------------------------------------------------------
    
    #Agrupamos
    
    Base_1= pd.concat([g_8, ng_3], axis= 0)
    
    Base_2= Base_1.sort_values(by= "EXPOSICIÓN BRUTA", ascending= False)
    
    Base_3= Base_2.reset_index()
    
    Base_Sin_SP_2= Base_3.drop(["index"], axis= "columns")
    
    Base_Sin_SP_2["NIVEL CONSOLID"]= "0"
    
    Base_Sin_SP_3= Base_Sin_SP_2[["TIPO ID", "CODIGO", "DENOMINACION", "NIVEL CONSOLID", "EXPOSICIÓN BRUTA", "EXPOSICIÓN NETA DE CRC", "EXPOSICIÓN NETA DE GTIAS A Y B"]]
    
    #--------------------------------------------------------------------------
    
    Base_Sin_SP_Temp= Base_Sin_SP_3.copy()
    
    Base_Sin_SP_Temp['CODIGO'] = Base_Sin_SP_Temp['CODIGO'].astype('int64')

    return Base_Sin_SP_Temp


#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------


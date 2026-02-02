import numpy as np
import pandas as pd
import sqlite3


#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------


def armado_cuadros(Base_Sin_SP_Temp, Cn1, Base_SP_def, ruta_bases, df_Individual_SV):

    Base_Sin_SP= Base_Sin_SP_Temp.copy()
    
    Base_Sin_SP["Comentario"]= np.where(Base_Sin_SP["EXPOSICIÓN BRUTA"] >= Cn1 * 0.15, "Exceso", "Otros")
    
    Exceso= Base_Sin_SP[Base_Sin_SP["Comentario"]== "Exceso"]
    
    Base_Sin_SP_1= Base_Sin_SP[Base_Sin_SP["Comentario"]!= "Exceso"]
    
    Base_Sin_SP_2= Base_Sin_SP_1.drop(["Comentario"], axis= "columns")
    
    Base_Sin_SP_2["TIPO DE EXPOSICIÓN"]= np.where(Base_Sin_SP_2["EXPOSICIÓN BRUTA"] >= Cn1 * 0.1, 1, 3)
    
    Base_1A= pd.concat([Base_Sin_SP_2, Base_SP_def], axis= 0)
    
    #-----------------------------------------------------------
    
    db= sqlite3.connect("{}/Bases/Maestros/maestro_grupos.db".format(ruta_bases))
    
    Maestro_1= pd.read_sql_query("SELECT * from maestro_grupos", db)
    
    db.close()
    
    Maestro_2= Maestro_1[Maestro_1["orden"]== 1]
    
    Mas_Usar= Maestro_2[["cuit", "denominacion", "codigo_grupo"]] 
    
    Base_1B= pd.merge(Base_1A, Mas_Usar, left_on= "CODIGO", right_on= "codigo_grupo", how= "left")
    
    Base_1B["DENOMINACION_x"]= np.where(Base_1B["TIPO ID"]== "88", Base_1B["denominacion"], Base_1B["DENOMINACION"])
    
    Base_1C= Base_1B.drop(["cuit", "DENOMINACION", "denominacion"], axis= "columns")
    
    Base_1= Base_1C.rename(columns={'DENOMINACION_x': 'DENOMINACION'})
    
    #-----------------------------------------------------------
    
    Base_2= Base_1.sort_values(by= "EXPOSICIÓN BRUTA", ascending= False)
    
    Base_3= Base_2.reset_index()
    
    Base_Completa= Base_3.drop(["index", "codigo_grupo"], axis= "columns")
    
    #Hacemos una nueva columna sólo para determinar si corresponde incluir más casos o no hasta llegar a los 20
    
    Base_Completa_1= Base_Completa.copy()
    
    Base_Completa_1["Control"]= np.where(Base_Completa_1["EXPOSICIÓN BRUTA"] >= Cn1 * 0.1, 1, 3)
    
    Base_Completa_2= Base_Completa_1[Base_Completa_1["Control"]== 1]
    
    Cant_Control= len(Base_Completa_2)
    
    if Cant_Control <= 20:
    
        Mayores_1= Base_Completa_1[0:20]
        
    else:
    
        Mayores_1= Base_Completa_1[Base_Completa_1["Control"]== 1]
    
    Mayores= Mayores_1.drop(["Control"], axis= "columns")
    
    Mayores['DENOMINACION'] = (Mayores['DENOMINACION'].replace('/,','', regex=True))
    
    #----------------------------------------------------------
    
    GE_1= Mayores[Mayores["TIPO ID"]== "88"]
    
    GE_2= GE_1["CODIGO"]
    
    GE_3A= pd.merge(GE_2, Maestro_1, left_on= "CODIGO", right_on= "codigo_grupo", how= "left")
    
    GE_3= GE_3A[["codigo_grupo", "cuit", "denominacion", "orden"]]
    
    GE_4= pd.merge(GE_3, df_Individual_SV, left_on= "cuit", right_on= "CUIT", how= "left")
    
    GE_5= GE_4.drop(["Denominación"], axis= "columns")
    
    GE_6= GE_5.fillna(0)
    
    GE_6["TIPO ID"]= 11
    
    GE_7= GE_6.sort_values(by= ["codigo_grupo", "orden"], ascending= [True, False])
    
    Maestro_3= Maestro_2[["codigo_grupo", "cuit"]]
    
    Maestro_4= Maestro_3.rename(columns={'cuit': 'CUIT_CLTE'})
    
    GE_8= pd.merge(GE_7, Maestro_4, on= "codigo_grupo", how= "left")
    
    GE_Completo_1= GE_8[["TIPO ID", "cuit", "denominacion", "codigo_grupo", "EXPOSICIÓN BRUTA", "EXPOSICIÓN NETA DE CRC", "EXPOSICIÓN NETA DE GTIAS A Y B", "CUIT_CLTE"]]
    
    GE_Completo= GE_Completo_1.rename(columns={'cuit': 'CUIT', 'denominacion': 'DENOMINACION', 'codigo_grupo': 'CODIGO'})
    
    GE_Completo['DENOMINACION'] = (GE_Completo['DENOMINACION'].replace('/,','', regex=True))
    
    return Base_Completa, Mayores, Exceso, GE_Completo


#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
#------------------------------------------------------------------------
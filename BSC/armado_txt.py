
import numpy as np
import pandas as pd
import sqlite3


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


def txt_BSF_Func(Base_BSF, fec_def, ruta_bases, nombre): 

    txt_1= Base_BSF.rename(columns={'TIPO ID': 'Tipo Ident Cliente', 'CODIGO': 'Nro Ident Cliente',
                                    'DENOMINACION': 'Denominación Cliente', 'SECTOR CLIENTE': 'Sector Cliente',
                                    'EXPOSICIÓN BRUTA': 'Exposición Bruta', 'EXPOSICIÓN NETA DE CRC': 'Exposición Neta CRC',
                                    'EXPOSICIÓN NETA DE GTIAS A Y B': 'Exposición Neta CRC y Gtías Pref'})
    
    txt_2a= txt_1[['Tipo Ident Cliente', 'Nro Ident Cliente', 'Denominación Cliente', 'Sector Cliente',
                  'Exposición Bruta', 'Exposición Neta CRC', 'Exposición Neta CRC y Gtías Pref']]
    
    txt_2= txt_2a.copy()
    
    txt_2['Sector Cliente']= txt_2['Sector Cliente'].astype(int) 
    
    txt_2["Nro Ident Cliente"]= np.where(((txt_2["Tipo Ident Cliente"]== 20) | (txt_2["Tipo Ident Cliente"]== 30)), 20, txt_2["Nro Ident Cliente"])
    
    txt_2['Exposición Bruta']= txt_2['Exposición Bruta'] * 1000
    
    txt_2['Exposición Bruta']= txt_2['Exposición Bruta'].round(2)
    
    txt_2['Exposición Bruta']= txt_2['Exposición Bruta'].astype(str)
    
    txt_2['Exposición Bruta']= txt_2['Exposición Bruta'].str.replace('.', ',', regex=False)
    
    txt_2['Exposición Bruta']= txt_2['Exposición Bruta'] + "0" 
    
    txt_2['Exposición Neta CRC']= txt_2['Exposición Neta CRC'] * 1000
    
    txt_2['Exposición Neta CRC'] = txt_2['Exposición Neta CRC'].round(2)
    
    txt_2['Exposición Neta CRC'] = txt_2['Exposición Neta CRC'].astype(str)
    
    txt_2['Exposición Neta CRC'] = txt_2['Exposición Neta CRC'].str.replace('.', ',', regex=False)
    
    txt_2['Exposición Neta CRC']= txt_2['Exposición Neta CRC'] + "0"
    
    txt_2['Exposición Neta CRC y Gtías Pref']= txt_2['Exposición Neta CRC y Gtías Pref'] * 1000
    
    txt_2['Exposición Neta CRC y Gtías Pref'] = txt_2['Exposición Neta CRC y Gtías Pref'].round(2)
    
    txt_2['Exposición Neta CRC y Gtías Pref'] = txt_2['Exposición Neta CRC y Gtías Pref'].astype(str)
    
    txt_2['Exposición Neta CRC y Gtías Pref'] = txt_2['Exposición Neta CRC y Gtías Pref'].str.replace('.', ',', regex=False)
    
    txt_2['Exposición Neta CRC y Gtías Pref']= txt_2['Exposición Neta CRC y Gtías Pref'] + "0"
        
    txt_3= txt_2.drop_duplicates()
    
    txt_3.to_csv("{}/Resultados/Consolidado/{}.txt".format(ruta_bases, nombre), sep=';', index= False, header= True)

    return 


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


def maestro_BSF_func(ruta_bases, fec_def, nombre):

    db= sqlite3.connect("{}/Bases/Maestros/maestro_grupos.db".format(ruta_bases))
    
    Maestro_1a= pd.read_sql_query("SELECT * from maestro_grupos", db)
    
    db.close()
    
    Maestro_1= Maestro_1a[["cuit", "denominacion", "codigo_grupo", "orden"]]
    
    Maestro_2= Maestro_1.rename(columns={'cuit': 'CUIT', 'denominacion': 'DENOMINACION', 
                                           'codigo_grupo': "CODIGO", "orden": "ORDEN"})
    
    lid_1= Maestro_2[Maestro_2["ORDEN"]== 1]
    
    lid_2= lid_1[["CODIGO", "DENOMINACION"]]
    
    Maestro_3= pd.merge(Maestro_2, lid_2, on= "CODIGO", how= "left")
    
    Maestro_3["Tipo Ident Integrante"]= 11
    
    Maestro_4= Maestro_3[["CODIGO", "DENOMINACION_y", "Tipo Ident Integrante", "CUIT", "DENOMINACION_x"]]
    
    Maestro_BSF= Maestro_4.rename(columns={'CODIGO': 'Nro Grupo', 'DENOMINACION_y': 'Denominación Grupo', 
                                           'CUIT': "Nro Ident Integrante", "DENOMINACION_x": "Denominación Integrante"})
    
    Maestro_BSF.to_csv("{}/Resultados/Consolidado/{}.txt".format(ruta_bases, nombre), sep=';', index= False, header= True)
    
    return


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


def Armado_TXT(Mayores, fec_def, ruta_bases, GE_Completo, nombre_1, nombre_2):

    TXT_Mayores_1= Mayores.copy()
    
    TXT_Mayores_1["EXPOSICIÓN BRUTA"]= TXT_Mayores_1['EXPOSICIÓN BRUTA'].astype(int)
    
    TXT_Mayores_1["EXPOSICIÓN NETA DE CRC"]= TXT_Mayores_1['EXPOSICIÓN NETA DE CRC'].astype(int)
    
    TXT_Mayores_1["EXPOSICIÓN NETA DE GTIAS A Y B"]= TXT_Mayores_1['EXPOSICIÓN NETA DE GTIAS A Y B'].astype(int)
    
    TXT_Mayores_1["CODIGO"]= np.where(((TXT_Mayores_1["TIPO ID"]== 20) | (TXT_Mayores_1["TIPO ID"]== 30)), 20, TXT_Mayores_1["CODIGO"])
    
    TXT_Mayores_1.to_csv("{}/Resultados/Local/{}.txt".format(ruta_bases, nombre_1), sep=';', index= False, header= False)
    
    TXT_GE_Completo_1= GE_Completo.copy()
    
    TXT_GE_Completo_1["EXPOSICIÓN BRUTA"]= TXT_GE_Completo_1['EXPOSICIÓN BRUTA'].astype(int)
    
    TXT_GE_Completo_1["EXPOSICIÓN NETA DE CRC"]= TXT_GE_Completo_1['EXPOSICIÓN NETA DE CRC'].astype(int)
    
    TXT_GE_Completo_1["EXPOSICIÓN NETA DE GTIAS A Y B"]= TXT_GE_Completo_1['EXPOSICIÓN NETA DE GTIAS A Y B'].astype(int)
    
    TXT_GE_Completo_1["Campo_Nulo_1"]= 0
    
    TXT_GE_Completo_1["Campo_Nulo_2"]= 0
    
    TXT_GE_Completo_1["Campo_Nulo_3"]= 0
    
    TXT_GE_Completo_1["Campo_Vacio_1"]= ""
    
    TXT_GE_Completo_1["Campo_Vacio_2"]= ""
    
    TXT_GE_Completo_1["Campo_Vacio_3"]= ""
    
    TXT_GE_Completo_2= TXT_GE_Completo_1[["CODIGO", "TIPO ID", "CUIT", "DENOMINACION", "EXPOSICIÓN BRUTA", "EXPOSICIÓN NETA DE CRC", "EXPOSICIÓN NETA DE GTIAS A Y B", "Campo_Nulo_1", "Campo_Nulo_2", "Campo_Nulo_3", "Campo_Vacio_1", "Campo_Vacio_2", "Campo_Vacio_3", "CUIT_CLTE"]]
    
    TXT_GE_Completo_2.to_csv("{}/Resultados/Local/{}.txt".format(ruta_bases, nombre_2), sep=';', index= False, header= False)

    return


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------




























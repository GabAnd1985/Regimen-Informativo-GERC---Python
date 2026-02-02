

import pandas as pd
import glob
from armado_xlsx import exportar_xlsx
from armado_txt import (txt_BSF_Func, maestro_BSF_func, Armado_TXT)


#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------


def extraer_numero(ruta_bases, fec_def):

    rute_consolidado= "{}/Resultados/Consolidado".format(ruta_bases)
    
    filelist= glob.glob("{}/*.txt".format(rute_consolidado))  
    
    newlist= []
    
    for file in filelist:
        newlist.append(file[0:])
        
    fechas_1= pd.DataFrame(newlist, columns= ["Fechas"])
    
    fechas_1["Var"]= fechas_1["Fechas"].str[(len(rute_consolidado) + 1):] 
    
    #--------------------------------------------------------------------
    
    rute_local= "{}/Resultados/Local".format(ruta_bases)
    
    filelist= glob.glob("{}/*.txt".format(rute_local))  
    
    newlist= []
    
    for file in filelist:
        newlist.append(file[0:])
        
    fechas_2= pd.DataFrame(newlist, columns= ["Fechas"])
    
    fechas_2["Var"]= fechas_2["Fechas"].str[(len(rute_local) + 1):]
    
    #--------------------------------------------------------------------
    
    filelist= glob.glob("{}/*.xlsx".format(rute_local))  
    
    newlist= []
    
    for file in filelist:
        newlist.append(file[0:])
        
    fechas_3= pd.DataFrame(newlist, columns= ["Fechas"])
    
    fechas_3["Var"]= fechas_3["Fechas"].str[(len(rute_local) + 1):]
    
    #--------------------------------------------------------------------
    
    fechas_4= pd.concat([fechas_1, fechas_2, fechas_3], axis= 0)
    
    if len(fechas_4)== 0:
        numero= 0
        return numero
    
    fechas_5= fechas_4[["Var"]]
    
    fec_1= fec_def[3:7] + fec_def[0:2]
    
    fechas_6a= fechas_5[fechas_5["Var"].astype(str).str.contains("{}".format(fec_1))]
    
    fechas_6= fechas_6a.copy()
    
    fechas_6["numero"] = fechas_6["Var"].str.extract(r"\((\d+)\)")
    
    fechas_7= fechas_6[["numero"]]
    
    fechas_8= fechas_7.fillna("0")
    
    numero= fechas_8["numero"].max()

    return numero


#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------


def export_files(ruta_bases, fec_def, Control_Maestro_Financiero, Mayores, Exceso, GE_Completo, Base_BSF):

    numero= extraer_numero(ruta_bases, fec_def)
    
    if numero== 0:
    
        fec_1= fec_def[3:7] + fec_def[0:2]
        
        Nombre= "GERC {}".format(fec_1)
        
        exportar_xlsx(ruta_bases, Control_Maestro_Financiero, Mayores, Exceso, GE_Completo, Nombre)
    
        Nombre_1= "EXPCLI {}".format(fec_1)
    
        txt_BSF_Func(Base_BSF, fec_def, ruta_bases, Nombre_1)
        
        Nombre_2= "GRUPOSECO {}".format(fec_1)
        
        maestro_BSF_func(ruta_bases, fec_def, Nombre_2)
    
        Nombre_3= "EXPOSICIONES {}".format(fec_1)
        
        Nombre_4= "GRUPOCONT {}".format(fec_1)
        
        Armado_TXT(Mayores, fec_def, ruta_bases, GE_Completo, Nombre_3, Nombre_4)
    
    else:
    
        fec_1= fec_def[3:7] + fec_def[0:2]    
    
        Nombre= "GERC {} ({}).xlsx".format(fec_1, (int(numero) + 1))
        
        exportar_xlsx(ruta_bases, Control_Maestro_Financiero, Mayores, Exceso, GE_Completo, Nombre)
    
        Nombre_1= "EXPCLI {} ({})".format(fec_1, (int(numero) + 1))
    
        txt_BSF_Func(Base_BSF, fec_def, ruta_bases, Nombre_1)
        
        Nombre_2= "GRUPOSECO {} ({})".format(fec_1, (int(numero) + 1))
        
        maestro_BSF_func(ruta_bases, fec_def, Nombre_2)
    
        Nombre_3= "EXPOSICIONES {} ({})".format(fec_1, (int(numero) + 1))
        
        Nombre_4= "GRUPOCONT {} ({})".format(fec_1, (int(numero) + 1))
        
        Armado_TXT(Mayores, fec_def, ruta_bases, GE_Completo, Nombre_3, Nombre_4)

    return 


#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
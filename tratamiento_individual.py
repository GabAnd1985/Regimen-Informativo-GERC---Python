
from utils.paths import definir_ruta_func
from solicitudes_usuario import validar_archivos_existen
import sqlite3
import pandas as pd
from importar_inputs import importar_input_manual


#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------


def armado_base_primera_func(path, fec, Input_Manual_input):

    fec_1= fec[3:7] + fec[0:2] 
    
    db= sqlite3.connect("{}/Bases/Deudores/Deudores_{}.db".format(path, fec_1))
    
    df_4305= pd.read_sql_query("SELECT * from d4305", db)
    
    df_4306= pd.read_sql_query("SELECT * from d4306", db)
    
    db.close()
    
    #Eliminamos lo que es sector público dado que será tratado de forma manual
    
    #3 es sector público no financiero
    
    #4 es sector público financiero
    
    df_1B= df_4305[df_4305["Residencia"]!= 3]
    
    df_1C= df_1B[df_1B["Residencia"]!= 4]
    
    df_1= df_1C[["CUIT", "Denominación", "Total Financiaciones"]]
    
    df_2= df_4306[["CUIT", "Gtias Pref A Capital Total", "Gtias Pref B Capital Total", "Gtias Pref B Intereses Total"]]
    
    cols = ["Gtias Pref A Capital Total", "Gtias Pref B Capital Total", "Gtias Pref B Intereses Total"]
    
    df_3= df_2.copy()
    
    df_3[cols]= df_3[cols].astype(float).fillna(0)
    
    df_3["Gtias Totales"]= df_3["Gtias Pref A Capital Total"] + df_3["Gtias Pref B Capital Total"] + df_3["Gtias Pref B Intereses Total"]
    
    df_4= df_3[["CUIT","Gtias Totales"]]
    
    grouped= df_4["Gtias Totales"].groupby(df_4["CUIT"])
    
    df_5= grouped.sum()
    
    df_6= pd.merge(df_1, df_5, on= "CUIT", how= "left")
    
    df_7= df_6.fillna(0)
    
    df_8= df_7.rename(columns= {"Total Financiaciones": "EXPOSICIÓN BRUTA"})
    
    df_8["EXPOSICIÓN NETA DE CRC"]= df_8["EXPOSICIÓN BRUTA"]
    
    df_8["EXPOSICIÓN NETA DE GTIAS A Y B"]= df_8["EXPOSICIÓN BRUTA"] - df_8["Gtias Totales"]
    
    df_Individual_1= df_8[["CUIT", "Denominación", "EXPOSICIÓN BRUTA", "EXPOSICIÓN NETA DE CRC", "EXPOSICIÓN NETA DE GTIAS A Y B"]]
    
    #Trabajamos ahora para incorporar el Input Manual
    
    Input_Manual_1= Input_Manual_input[['CODIGO', 'DENOMINACION', 'EXPOSICIÓN BRUTA', 'EXPOSICIÓN NETA DE CRC', 'EXPOSICIÓN NETA DE GTIAS A Y B']]
    
    Input_Manual_2= Input_Manual_1.rename(columns={'CODIGO': 'CUIT', 'DENOMINACION': 'Denominación'})
    
    #Apendamos el input manual con la base ya trabajada
    
    df_Individual_2= pd.concat([df_Individual_1, Input_Manual_2], axis= 0)
    
    df_Individual_3= df_Individual_2.groupby(['CUIT'])[['EXPOSICIÓN BRUTA', 'EXPOSICIÓN NETA DE CRC', "EXPOSICIÓN NETA DE GTIAS A Y B"]].sum().reset_index()
    
    #En caso que haya conflictos por diferente nombre entre el input manual y los diseños, ajusto
    
    Name_1= df_Individual_2[["CUIT", "Denominación"]]
    
    Name_2= Name_1.sort_values(by= "CUIT", ascending= True)
    
    Name_3= Name_2.drop_duplicates(["CUIT"], keep= "first")
    
    df_Individual_4= pd.merge(df_Individual_3, Name_3, on= "CUIT", how= "left")
        
    df_Individual_FV= df_Individual_4[["CUIT", "Denominación", "EXPOSICIÓN BRUTA", "EXPOSICIÓN NETA DE CRC", "EXPOSICIÓN NETA DE GTIAS A Y B"]]

    return df_Individual_FV


#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------


def main():

    fec_def= validar_archivos_existen()
    
    ruta_bases= definir_ruta_func()
    
    Input_Manual= importar_input_manual(ruta_bases, fec_def)
    
    df_Individual_FV= armado_base_primera_func(ruta_bases, fec_def, Input_Manual)

    return df_Individual_FV


#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------


if __name__ == "__main__":
    main()
































#
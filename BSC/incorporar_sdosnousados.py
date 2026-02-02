
import pandas as pd


#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------


#Agregamos los saldos no usados Algunos clientes pueden ya estar, otros deben ser agregados

def agreg_sdos_nousados_func(Acc_Incorporar, TC_Incorporar, df_Individual_FV):

    Acc_Incorporar_1= Acc_Incorporar.copy()
    
    Acc_Incorporar_1["Acc_Incorporar_1"]= Acc_Incorporar_1["Acc_Incorporar"] / 1000
    
    Acc_Incorporar_1["EXPOSICIÓN BRUTA"]= Acc_Incorporar_1["Acc_Incorporar_1"]
    
    Acc_Incorporar_1["EXPOSICIÓN NETA DE CRC"]= Acc_Incorporar_1["Acc_Incorporar_1"]
    
    Acc_Incorporar_1["EXPOSICIÓN NETA DE GTIAS A Y B"]= Acc_Incorporar_1["Acc_Incorporar_1"]
    
    Acc_Incorporar_2= Acc_Incorporar_1.drop(["Acc_Incorporar", "Acc_Incorporar_1"], axis= "columns")
    
    #----------------------------------------------------------------------------
    
    TC_Incorporar_1= TC_Incorporar.copy()
    
    TC_Incorporar_1["TC_Incorporar_1"]= TC_Incorporar_1["TC_Incorporar"] / 1000
    
    TC_Incorporar_1["EXPOSICIÓN BRUTA"]= TC_Incorporar_1["TC_Incorporar_1"]
    
    TC_Incorporar_1["EXPOSICIÓN NETA DE CRC"]= TC_Incorporar_1["TC_Incorporar_1"]
    
    TC_Incorporar_1["EXPOSICIÓN NETA DE GTIAS A Y B"]= TC_Incorporar_1["TC_Incorporar_1"]
    
    TC_Incorporar_2= TC_Incorporar_1.drop(["TC_Incorporar_1", "TC_Incorporar"], axis= "columns")
    
    TC_Incorporar_3= TC_Incorporar_2.rename(columns={'id_cliente': 'CUIT'})
    
    #----------------------------------------------------------------------------
    
    df_Individual_01= pd.merge(df_Individual_FV, Acc_Incorporar_2, on= "CUIT", how= "left")
    
    df_Individual_02= pd.merge(df_Individual_01, TC_Incorporar_3, on= "CUIT", how= "left")
    
    df_Individual_03= df_Individual_02.fillna(0)
    
    df_Individual_03["EXPOSICIÓN BRUTA def"]= df_Individual_03["EXPOSICIÓN BRUTA"] + df_Individual_03["EXPOSICIÓN BRUTA_x"] + df_Individual_03["EXPOSICIÓN BRUTA_y"]
    
    df_Individual_03["EXPOSICIÓN NETA DE CRC def"]= df_Individual_03["EXPOSICIÓN NETA DE CRC"] + df_Individual_03["EXPOSICIÓN NETA DE CRC_x"] + df_Individual_03["EXPOSICIÓN NETA DE CRC_y"]
    
    df_Individual_03["EXPOSICIÓN NETA DE GTIAS A Y B def"]= df_Individual_03["EXPOSICIÓN NETA DE GTIAS A Y B"] + df_Individual_03["EXPOSICIÓN NETA DE GTIAS A Y B_x"] + df_Individual_03["EXPOSICIÓN NETA DE GTIAS A Y B_y"]
    
    df_Individual_04= df_Individual_03[["CUIT", "Denominación", "EXPOSICIÓN BRUTA def", "EXPOSICIÓN NETA DE CRC def", "EXPOSICIÓN NETA DE GTIAS A Y B def"]]
    
    df_Individual_SV= df_Individual_04.rename(columns= {"EXPOSICIÓN BRUTA def": "EXPOSICIÓN BRUTA", "EXPOSICIÓN NETA DE CRC def": "EXPOSICIÓN NETA DE CRC", "EXPOSICIÓN NETA DE GTIAS A Y B def": "EXPOSICIÓN NETA DE GTIAS A Y B"})
    
    return df_Individual_SV


#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------


def main(Acc_Incorporar, TC_Incorporar, df_Individual_FV):
    
    df_Individual_SV= agreg_sdos_nousados_func(Acc_Incorporar, TC_Incorporar, df_Individual_FV)
    
    return df_Individual_SV


#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------


if __name__ == "__main__":
    main()
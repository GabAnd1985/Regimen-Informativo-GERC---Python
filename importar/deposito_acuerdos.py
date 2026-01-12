
import pandas as pd
import numpy as np
import sqlite3
from utils.paths import definir_ruta_func
from utils.validaciones import validar_archivos_existen

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------


def ACMAC_tabla_func(path, fec):

    df_1= pd.read_table("{}/Inputs/Acuerdos/ACMAC {}.txt".format(path, fec), 
                        names= ["Tipo", "Moneda", "Sucursal", "Producto", "Cuenta", "Acuerdo", "Estado", "Digito", "Fecha_Inicio",
                                "Vto_Acuerdo", "Monto_Acuerdo"], sep= "~", 
                        usecols= [1, 2, 3, 4, 5, 6, 9, 12, 16, 20, 28])
    
    
    df_1["Fecha_Inicio_v1"]= np.where(df_1["Fecha_Inicio"] < 100000, "0" + df_1["Fecha_Inicio"].astype(str), df_1["Fecha_Inicio"].astype(str)) 
    
    df_1["Fecha_Inicio_v2"]= pd.to_datetime(df_1["Fecha_Inicio_v1"], format='%d%m%y') 
    
    df_1["Fecha_Inicio_v3"]= df_1["Fecha_Inicio_v2"].dt.date
    
    df_1["Fecha_Ref"]= df_1["Fecha_Inicio_v3"].astype(str).str[0:4] + df_1["Fecha_Inicio_v3"].astype(str).str[5:7]
    
    df_1["Fecha_Ref"]= df_1["Fecha_Ref"].astype(int)
    
    Fecha_var= fec[3:7] + fec[0:2] 
    
    df_2= df_1[df_1["Fecha_Ref"] <= int(Fecha_var)]
    
    ACMAC_tabla_temp= df_2.drop(["Fecha_Inicio_v1", "Fecha_Inicio_v2", "Fecha_Inicio_v3", "Fecha_Ref"], axis= "columns")

    return ACMAC_tabla_temp


#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------


def cruce_ACMOL_func(path, fec):

    ACMAC_tabla_temp= ACMAC_tabla_func(path, fec)

    df_1= pd.read_table("{}/Inputs/Acuerdos/ACMOL {}.txt".format(path, fec), 
                        names= ["Moneda", "Sucursal", "Producto", "Cuenta", "DigVerificador", "NroSFB"], sep= "~", 
                        usecols= [1, 2, 3, 4, 59, 172], encoding='latin-1')
    
    df_2= pd.merge(ACMAC_tabla_temp, df_1, left_on= ["Moneda", "Sucursal", "Producto", "Cuenta", "Digito"], right_on= ["Moneda", "Sucursal", "Producto", "Cuenta", "DigVerificador"], how= "left")
    
    df_3= df_2.dropna(subset=['NroSFB'])
    
    Acc_tabla= df_3.drop(["DigVerificador"], axis= "columns")
    
    return Acc_tabla


#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------


def Deposito_Acuerdos_Func(path, fec):

    Tabla= cruce_ACMOL_func(path, fec)

    db = sqlite3.connect("{}/Bases/Acuerdos/ACMAC_{}.db".format(path, fec))
    
    Tabla.to_sql('ACMAC', db, index=False, if_exists='replace')
    
    db.close()
    
    return


#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------


def main():
    
    fec_def= validar_archivos_existen()
    
    ruta_bases= definir_ruta_func()

    Deposito_Acuerdos_Func(ruta_bases, fec_def)
    
    return


#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------


if __name__ == "__main__":
    main()












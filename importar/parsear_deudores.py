
import sqlite3


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------


def parsear_deudores_func(base):
    
    df_1= base[base[0]== 4305]
    
    df_2= df_1.drop([27, 28], axis= "columns") 
    
    df_4305= df_2.rename(columns= {0: "Diseño", 1: "Tipo_Ident", 2: "CUIT", 3: "Denominación", 4: "Categoría", 5: "Residencia", 6: "Gobierno", 
                                7: "Provincia", 8: "Situación", 9: "Vinculación", 10: "Previsión Asist Crediticia", 11: "Previsión Particip",
                                12: "Previsión Responsab", 13: "Incremento Previsiones General", 14: "Incremento Previsiones Opcion",
                                15: "Asistencia Vinculados", 16: "Total Financiaciones", 17: "Actividad Principal", 
                                18: "Información Transitoria", 19: "Deudor Encuadrado", 20: "Refinanciaciones", 21: "Recateg_Obligatoria",
                                22: "Sit Jurídica", 23: "Irrecup Disp Técnica", 24: "Días Atraso", 25: "Mipyme",
                                26: "Sit Sin Reclasificación"})
    
    df_4= base[base[0]== 4306]
    
    df_5= df_4.drop([17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28], axis= "columns") 
    
    df_4306= df_5.rename(columns= {0: "Diseño", 1: "Tipo_Ident", 2: "CUIT", 3: "Tipo Asistencia", 4: "Gtias Pref A Capital Vencida",
                                   5: "Gtias Pref A Capital Total", 6: "Gtias Pref B Capital Vencida", 7: "Gtias Pref B Capital Total",
                                   8: "Gtias Pref B Intereses Vencida", 9: "Gtias Pref B Intereses Total", 10: "Sin Gtias Pref Cap Vencida",
                                   11: "Sin Gtias Pref Cap Total", 12: "Sin Gtias Pref Interes Vencida", 13: "Sin Gtia Pref Interes Total",
                                   14: "Previsiones Minimas", 15: "Fecha Refinanc", 16: "Financiacion Mipyme"})
    
    return df_4305, df_4306


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------


def Reserva_SQL_Func(df, path_input, fec):
    
    df_4305, df_4306= parsear_deudores_func(df)
    
    fec_1= fec[3:7] + fec[0:2] 
    
    db= sqlite3.connect("{}/Deudores_{}.db".format(path_input, fec_1))
    
    df_4305.to_sql('d4305', db, index=False, if_exists='replace')
    
    df_4306.to_sql('d4306', db, index=False, if_exists='replace')
    
    db.close()

    return


#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#----------------------------------------------------------------------




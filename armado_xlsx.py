

import pandas as pd


#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------


def exportar_xlsx(ruta_bases, Control_Maestro_Financiero, Mayores, Exceso, GE_Completo, Nombre):

    with pd.ExcelWriter("{}/Resultados/Local/{}.xlsx".format(ruta_bases, Nombre)) as writer:  
         Control_Maestro_Financiero.to_excel(writer, sheet_name='Control Mto Fciero', index= False)
         Mayores.to_excel(writer, sheet_name='Mayores', index= False)
         Exceso.to_excel(writer, sheet_name='Exceso', index= False)
         GE_Completo.to_excel(writer, sheet_name='GE_Completo', index= False)

    return
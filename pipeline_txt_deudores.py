
from importar_inputs import (importar_deudores_func, importar_RD_MP_func, importar_input_manual, importar_sp_func)
from importar.deposito_acuerdos import Deposito_Acuerdos_Func
from utils.paths import definir_ruta_func
from solicitudes_usuario import (validar_archivos_existen, solicitud_Cn1_func)
from tratamiento_individual import armado_base_primera_func
from tratamiento_acuerdos import armado_acuerdos_func
from tratamiento_tc import armado_tc_func
from armado_sin_sp import armado_sin_sp_func
from config.config_local import Ruta_SAS
from incorporar_sdosnousados import agreg_sdos_nousados_func
from base_sp import (base_sp_func, deuda_tc_sp)
from armar_cuadros import armado_cuadros
from armado_bsf import armado_BSF
from exportar_archivos import export_files


#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------


def generate_txt_func():
    
    fec_def= validar_archivos_existen()
    
    ruta_bases= definir_ruta_func()
    
    importar_deudores_func(ruta_bases, fec_def)
    
    Input_Manual= importar_input_manual(ruta_bases, fec_def)
    
    RD_MP= importar_RD_MP_func(ruta_bases, fec_def)
    
    SP, lim_TC_SP= importar_sp_func(ruta_bases, fec_def)
    
    Deposito_Acuerdos_Func(ruta_bases, fec_def)
    
    df_Individual_FV= armado_base_primera_func(ruta_bases, fec_def, Input_Manual)
    
    Acc_Incorporar= armado_acuerdos_func(ruta_bases, fec_def, RD_MP)
    
    TC_Incorporar= armado_tc_func(fec_def, Ruta_SAS)
    
    df_Individual_SV= agreg_sdos_nousados_func(Acc_Incorporar, TC_Incorporar, df_Individual_FV) 
    
    Base_Sin_SP_Temp= armado_sin_sp_func(df_Individual_FV, ruta_bases)
    
    Deuda_TC_SP= deuda_tc_sp(ruta_bases, fec_def)
    
    Cn1= int(solicitud_Cn1_func())
    
    Base_SP_def= base_sp_func(Cn1, lim_TC_SP, Deuda_TC_SP, SP)
    
    Base_Completa, Mayores, Exceso, GE_Completo= armado_cuadros(Base_Sin_SP_Temp, Cn1, Base_SP_def, ruta_bases, df_Individual_SV)
    
    Control_Maestro_Financiero, Base_BSF= armado_BSF(ruta_bases, Base_Completa, df_Individual_SV, fec_def)
    
    export_files(ruta_bases, fec_def, Control_Maestro_Financiero, Mayores, Exceso, GE_Completo, Base_BSF)
    
    return


#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
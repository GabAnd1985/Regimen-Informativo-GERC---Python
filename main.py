
from opciones import opciones_principales_func
from importar_inputs import (importar_deudores_func, importar_RD_MP_func, importar_input_manual, importar_sp_func,
                             TC_Sdo_No_Usado_Func)
from importar.deposito_acuerdos import Deposito_Acuerdos_Func
from utils.paths import definir_ruta_func
from solicitudes_usuario import validar_archivos_existen
from grupos_economicos import (crear_tabla_maestro_grupos, alta_clientes_func, baja_clientes_func, exportar_maestro_func, 
                               importar_base_func, mostrar_tabla_func)
from opciones import opciones_ge
from tratamiento_individual import armado_base_primera_func
from tratamiento_acuerdos import armado_acuerdos_func
from tratamiento_tc import armado_tc_func
from armado_sin_sp import armado_sin_sp_func
from config.config_local import Ruta_SAS
from incorporar_sdosnousados import agreg_sdos_nousados_func
from base_sp import (base_sp_func, deuda_tc_sp)


#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------

eleccion= opciones_principales_func()

if eleccion== "1":
    
    fec_def= validar_archivos_existen()
    
    ruta_bases= definir_ruta_func()
    
    importar_deudores_func(ruta_bases, fec_def)
    
    Input_Manual= importar_input_manual(ruta_bases, fec_def)
    
    RD_MP= importar_RD_MP_func(ruta_bases, fec_def)
    
    SP, lim_TC_SP= importar_sp_func(ruta_bases, fec_def)
    
    TC_Sdo_No_Usado= TC_Sdo_No_Usado_Func(fec_def)
    
    Deposito_Acuerdos_Func(ruta_bases, fec_def)
    
    df_Individual_FV= armado_base_primera_func(ruta_bases, fec_def, Input_Manual)
    
    Acc_Incorporar= armado_acuerdos_func(ruta_bases, fec_def, RD_MP)
    
    TC_Incorporar= armado_tc_func(fec_def, Ruta_SAS)
    
    df_Individual_SV= agreg_sdos_nousados_func(Acc_Incorporar, TC_Incorporar, df_Individual_FV) 
    
    Base_Sin_SP_Temp= armado_sin_sp_func(df_Individual_FV, ruta_bases)
    
    Deuda_TC_SP= deuda_tc_sp(ruta_bases, fec_def)
    
    Base_SP_def= base_sp_func(lim_TC_SP, Deuda_TC_SP, SP)
    
    
elif eleccion== "2":
    
    crear_tabla_maestro_grupos()
    
    eleccion= opciones_ge()
    
    if eleccion== "1":
        alta_clientes_func()
    elif eleccion== "2":
        baja_clientes_func()
    elif eleccion== "3":
        exportar_maestro_func()
    elif eleccion== "4":
        importar_base_func()
    elif eleccion== "5":
        mostrar_tabla_func()
        
        
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------

fec_def= validar_archivos_existen()

ruta_bases= definir_ruta_func()

importar_deudores_func(ruta_bases, fec_def)

Input_Manual= importar_input_manual(ruta_bases, fec_def)

RD_MP= importar_RD_MP_func(ruta_bases, fec_def)

SP, lim_TC_SP= importar_sp_func(ruta_bases, fec_def)

TC_Sdo_No_Usado= TC_Sdo_No_Usado_Func(fec_def)

Deposito_Acuerdos_Func(ruta_bases, fec_def)

df_Individual_FV= armado_base_primera_func(ruta_bases, fec_def, Input_Manual)

Acc_Incorporar= armado_acuerdos_func(ruta_bases, fec_def, RD_MP)

TC_Incorporar= armado_tc_func(fec_def)

Base_Sin_SP_Temp= armado_sin_sp_func(df_Individual_FV, ruta_bases)

Deuda_TC_SP= deuda_tc_sp(ruta_bases, fec_def)

Base_SP_def= base_sp_func(lim_TC_SP, Deuda_TC_SP, SP)
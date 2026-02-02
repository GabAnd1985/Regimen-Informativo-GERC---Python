
import sqlite3
import pandas as pd
from utils.paths import definir_ruta_func
from utils.validaciones import selector
from utils.validaciones import selector_num
from utils.validaciones import validacion_si_no
from datetime import datetime
from tabulate import tabulate
from opciones import opciones_ge
import sys


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


def crear_tabla_clientes_financieros():
    """Cree la base de clientes financieros y la tabla con las columnas adecuadas
        en caso de que no exista"""
    
    sql = """
    CREATE TABLE IF NOT EXISTS maestro_clientes_financieros (
        id              INTEGER PRIMARY KEY,
        cuit            TEXT NOT NULL,
        denominacion    TEXT    NOT NULL,
        sector          INTEGER NOT NULL CHECK (sector IN (2,4)),
        UNIQUE (cuit)
    );
    """

    ruta_bases= definir_ruta_func()

    db_path = ruta_bases / "Bases" / "Maestros" / "maestro_clientes_financieros.db"

    with sqlite3.connect(db_path) as conn:
        conn.execute(sql)

    return


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


def alta_clientes_fcieros_func():
    
    continua= "s"
    
    ruta_bases= definir_ruta_func()
    
    db_path = ruta_bases / "Bases" / "Maestros" / "maestro_clientes_financieros.db"
    
    while continua== "s":
    
        cuit= selector_num("Ingrese el CUIT del cliente")
        
        deno= input("\nIngrese el nombre del cliente: ").upper()
        
        deno= deno.replace("Ñ", "N")
        
        codigo= selector("Ingrese 2 si es Privado Finaciero y 4 si es Público Financiero", 2, 4)
            
        sql = """
        INSERT INTO maestro_clientes_financieros (
            cuit,
            denominacion,
            sector
        )
        VALUES (?, ?, ?);
        """
        
        try:
        
            with sqlite3.connect(db_path) as conn:
                conn.execute(sql, (cuit, deno, codigo))
                
        except sqlite3.IntegrityError:
            print("\nEl CUIT ya existe para este maestro, no se insertó el registro.")
    
        continua= validacion_si_no("¿Desea agregar otro cliente?")      

    return 


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


def baja_clientes_fcieros_func():
    
    ruta_bases= definir_ruta_func()
    
    db_path = ruta_bases / "Bases" / "Maestros" / "maestro_clientes_financieros.db"
    
    continua= "s"
    
    while continua== "s":
    
        id_1= selector_num("Ingrese el id del cliente")
        
        print("\nDesea eliminar el registro siguiente?")
        
        db= sqlite3.connect("{}".format(db_path))
    
        eliminate_1= pd.read_sql_query("SELECT * FROM maestro_clientes_financieros WHERE id= '{}';".format(id_1), db)
        
        print("")
        
        print(tabulate(eliminate_1, headers="keys", tablefmt="psql", showindex=False))
        
        confirm= input("\nPresione s/n: ")
        
        while confirm not in ("s","n", "S", "N"):
        
            print("\n entrada incorrecta")    
        
            confirm= input("\nPresione s/n: ")
        
        if confirm in ("s", "S"):
        
            sql= "DELETE FROM maestro_clientes_financieros WHERE id = ?;"
            
            with sqlite3.connect(db_path) as conn:
                conn.execute(sql, (id_1,))
                
        else:
            
            pass
        
        continua= validacion_si_no("\nDesea eliminar otro cliente?")    

    return


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


def exportar_maestro_fcieros_func():

    ruta_bases= definir_ruta_func()
    
    db_path = ruta_bases / "Bases" / "Maestros" / "maestro_clientes_financieros.db"
        
    db = sqlite3.connect(db_path)
    
    table_1= pd.read_sql_query("SELECT * from maestro_clientes_financieros", db)
    
    db.close()
    
    ahora= str(datetime.now())
    
    ahora_1= ahora[0:4] + ahora[5:7] + ahora[8:10] + "_" + ahora[11:13] + ahora[14:16] + ahora[17:19] 
    
    db_path_1 = ruta_bases / "Resultados" / "Maestro Grupos" / "maestro_clientes_financieros_{}.xlsx".format(ahora_1)
    
    table_1.to_excel(db_path_1, index=False)

    return 


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


def importar_base_fcieros_func():

    ruta_bases= definir_ruta_func()
    
    db_path= ruta_bases / "Inputs" / "Maestros" / "Maestro_Financiero.xlsx"
    
    try:
        
        tabla_1= pd.read_excel(db_path)
    
    except:
        
        print("\nLa base de maestros clientes financieros no se encuentra")
        
        print("\nEl programa se da por finalizado")
        
        input("\npresione 'enter' para salir...")
        
        sys.exit()
    
    cols_1= list(tabla_1.columns)
    
    if "CUIT" not in cols_1:
        print("\nEl campo CUIT no se encuentra en los nombres de las columnas")
        return
    if "DENOMINACION" not in cols_1:
        print("\nEl campo DENOMINACION no se encuentra en los nombres de las columnas")
        return
    if "SECTOR" not in cols_1:
        print("\nEl campo SECTOR no se encuentra en los nombres de las columnas")
        return
    
    tabla_2= tabla_1[["CUIT", "DENOMINACION", "SECTOR"]]
    
    tabla_3= tabla_2.rename(columns= {"CUIT": "cuit", "DENOMINACION": "denominacion", "SECTOR": "sector"})
    
    ruta_bases= definir_ruta_func()
    
    db_path_1= ruta_bases / "Bases" / "Maestros" / "maestro_clientes_financieros.db"
    
    db = sqlite3.connect(db_path_1)
    
    cuits_1= pd.read_sql_query("SELECT distinct cuit from maestro_clientes_financieros", db)
    
    db.close()
    
    cuits_1["repetida"]= True
    
    cuits_1["cuit"]= cuits_1["cuit"].astype(int)
    
    tabla_4= pd.merge(tabla_3, cuits_1, on= "cuit", how= "left")
    
    tabla_5= tabla_4[tabla_4["repetida"]== True]
    
    if len(tabla_5) >= 1:
        print("\nUn cliente del excel ya se encuentra en la Base de datos")
        return
    
    db = sqlite3.connect(db_path_1)
    
    tabla_3.to_sql('maestro_clientes_financieros', db, index=False, if_exists='append')
    
    db.close()

    return


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


def mostrar_tabla_fcieros_func():

    ruta_bases= definir_ruta_func()
    
    db_path = ruta_bases / "Bases" / "Maestros" / "maestro_clientes_financieros.db"
        
    db = sqlite3.connect(db_path)
    
    table_1= pd.read_sql_query("SELECT * from maestro_clientes_financieros", db)
    
    db.close()
    
    table_2= table_1.rename(columns= {"id": "Id", "cuit": "CUIT", "denominacion": "Denominación",
                                      "sector": "Sector"})
    
    print("")
    
    print(tabulate(table_2, headers="keys", tablefmt="psql", showindex=False))

    return


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------


def main():

    crear_tabla_clientes_financieros()
    
    eleccion= opciones_ge()
    
    if eleccion== "1":
        alta_clientes_fcieros_func()
    elif eleccion== "2":
        baja_clientes_fcieros_func()
    elif eleccion== "3":
        exportar_maestro_fcieros_func()
    elif eleccion== "4":
        importar_base_fcieros_func()
    elif eleccion== "5":
        mostrar_tabla_fcieros_func()

    return


#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------


if __name__ == "__main__":
    main()
    

#Mejoras Pendientes

#Enviar mail con las novedades (consultar previo al envío) los que sea gregan y eliminan



















#



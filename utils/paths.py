
from pathlib import Path


#--------------------------------------------------------------
#--------------------------------------------------------------
#--------------------------------------------------------------
#--------------------------------------------------------------

def definir_ruta_func():

    """
    Devuelve el directorio base del proyecto.
    - En ejecución normal: raíz del repo/proyecto (padre de /utils).
    - En entornos donde __file__ no existe (ej. notebook): directorio actual.    
    """

    try:
        base_dir= Path(__file__).resolve().parent.parent
    except NameError:
        base_dir= Path().resolve().parent
        
    return base_dir 


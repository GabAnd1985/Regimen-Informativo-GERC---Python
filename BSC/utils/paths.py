
from pathlib import Path
import sys


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

    #try:
    #    base_dir= Path(__file__).resolve().parent.parent
    #except NameError:
    #    base_dir= Path().resolve().parent
    #    
    
    if getattr(sys, "frozen", False):
        # exe: .../RI_GERC_portable/RI_GERC/RI_GERC.exe -> subo a RI_GERC_portable
        return Path(sys.executable).resolve().parents[2]

    # script normal
    #return Path(__file__).resolve().parent.parent
    #return base_dir 

    return Path(__file__).resolve().parent.parent



from datetime import datetime
import re

def data_valida(data_str, formato="%d/%m/%Y"):
    try:
        datetime.strptime(data_str, formato)
        return True
    except ValueError:
        return False

def codigo_valido(codigo: str):
    padrao = r"^[A-Z]{4}\d{1,2}$"
    return bool(re.match(padrao, codigo))
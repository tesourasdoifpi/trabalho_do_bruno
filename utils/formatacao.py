import datetime

def formata_valor(valor: float) -> float:
  return round(valor, 2)

def formatar_data_do_banco(data_obj):
    if isinstance(data_obj, datetime.date):
        return data_obj.strftime("%d/%m/%Y")
    return None

from datetime import datetime

#Função que recebe dois parâmetros: uma data e um formato e retorna se ela é válida
def data_valida(data_str, formato="%d/%m/%Y"):
    """
    Função para validar se uma string é uma data real.
    - data_str: A string contendo a data (ex: "25/12/2026")
    - formato: O formato esperado da data (padrão brasileiro: dia/mês/ano)
    """
    try:
        # Tenta converter a string em um objeto datetime usando o formato fornecido.
        # Se a data for inválida (ex: 31/02), o Python gera um ValueError.
        datetime.strptime(data_str, formato)
        return True
    except ValueError:
        # Se ocorreu um erro na conversão, a data é inválida.
        return False


def codigo_valido(codigo: str) -> bool:
    """
    Função para validar um código textual.
    Regras:
    1. Deve ser uma string.
    2. O tamanho deve ser de 5 ou 6 caracteres.
    3. Os primeiros 4 caracteres devem ser letras maiúsculas.
    4. Os caracteres restantes devem ser números.
    """
    # Verifica se o código é uma string e se o tamanho está entre 5 e 6 caracteres
    if not (isinstance(codigo, str) and 5 <= len(codigo) <= 6):
        return False

    # Separa o prefixo (primeiros 4 caracteres) e o sufixo (o restante)
    prefixo = codigo[:4]
    sufixo = codigo[4:]
    
    # prefixo.isalpha(): verifica se são apenas letras
    # prefixo.isupper(): verifica se todas as letras são maiúsculas
    # sufixo.isdigit(): verifica se todos os caracteres do sufixo são números
    return prefixo.isalpha() and prefixo.isupper() and sufixo.isdigit()

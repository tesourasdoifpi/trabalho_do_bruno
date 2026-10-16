from flask import render_template, request, redirect, url_for
from models.operacao import Operacao


def _tratar_dados_formulario(form):
    """Converte os campos numéricos vindos do formulário HTML para os tipos corretos (int/float)."""
    dados = dict(form)
    try:
        if "quantidade" in dados and dados["quantidade"]:
            dados["quantidade"] = int(dados["quantidade"])
    except ValueError:
        pass

    try:
        if "valor_unitario" in dados and dados["valor_unitario"]:
            dados["valor_unitario"] = float(dados["valor_unitario"])
    except ValueError:
        pass

    try:
        if "tipo_operacao" in dados and dados["tipo_operacao"]:
            dados["tipo_operacao"] = int(dados["tipo_operacao"])
    except ValueError:
        pass

    return dados


def exibir_erros(erros: list):
    # Passando diretamente a lista para facilitar o loop no template Jinja
    return render_template("erros.html", erros=erros)


def listar_todas_operacoes():
    operacoes = Operacao.get_operacoes()
    return render_template("operacoes.html", operacoes=operacoes)


def cadastrar_operacao():
    if request.method == 'GET':
        return render_template("nova_operacao.html")

    elif request.method == 'POST':
        # Converte strings do form para int/float antes de instanciar o modelo
        dados = _tratar_dados_formulario(request.form)
        nova_operacao = Operacao(dados=dados)
        
        if nova_operacao.validate():
            nova_operacao.save()
            return redirect(url_for('listar_todas_operacoes'))
        else:
            return exibir_erros(erros=nova_operacao.errors)


def visualizar_operacao(id):
    operacao_dict = Operacao.pegar_por_id(id)
    if operacao_dict:
        # Instancia o objeto Operacao para aproveitar as propriedades no template
        operacao = Operacao(operacao_dict)
        return render_template("detalhar_operacao.html", operacao=operacao)
    return "Operação não encontrada", 404


def apagar_operacao(id):
    operacao_dict = Operacao.pegar_por_id(id)
    if operacao_dict:
        operacao = Operacao(operacao_dict)
        operacao.apagar()
    return redirect(url_for('listar_todas_operacoes'))


def editar_operacao(id):
    operacao_dict = Operacao.pegar_por_id(id)
    if not operacao_dict:
        return "Operação não encontrada", 404

    if request.method == 'GET':
        operacao = Operacao(operacao_dict)
        return render_template("editar_operacao.html", operacao=operacao)

    elif request.method == 'POST':
        dados = _tratar_dados_formulario(request.form)
        dados["id"] = int(id) # Garante que o ID permaneça o mesmo ao editar

        operacao = Operacao(dados=dados)
        if operacao.validate():
            operacao.atualizar()
            return redirect(url_for('listar_todas_operacoes'))
        else:
            return exibir_erros(erros=operacao.errors)


def pesquisa():
    return render_template("pesquisa.html")

def resultado_pesquisa():
    """Recebe os dados do formulário (GET), busca no banco e renderiza os resultados."""
    tipo_pesquisa = request.args.get("tipo_pesquisa")
    operacoes = []
    mensagem = ""

    if tipo_pesquisa == "termo":
        termo = request.args.get("termo_busca")
        if termo:
            operacoes = Operacao.pesquisa_por_termo(termo)
            mensagem = f"Resultados da pesquisa por código/ID: '{termo}'"

    elif tipo_pesquisa == "data":
        data_inicio = request.args.get("data_inicio")
        data_fim = request.args.get("data_fim")
        if data_inicio and data_fim:
            operacoes = Operacao.pesquisa_por_data(data_inicio, data_fim)
            # Você pode formatar a data para exibição se desejar (ex: dd/mm/aaaa)
            mensagem = f"Resultados no período de {data_inicio} até {data_fim}"

    # Reutilizamos o template operacoes.html passando a lista filtrada e a mensagem
    return render_template("operacoes.html", operacoes=operacoes, titulo_pagina="Resultados da Pesquisa", mensagem=mensagem)

# Se você estiver usando o app.route diretamente nas funções, adicione-os assim:
# app.add_url_rule('/pesquisa', view_func=pesquisa, methods=['GET'])
# app.add_url_rule('/resultado_pesquisa', view_func=resultado_pesquisa, methods=['GET'])
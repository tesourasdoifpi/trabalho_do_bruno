from controllers.operacao_controller import listar_todas_operacoes, cadastrar_operacao, apagar_operacao, visualizar_operacao, editar_operacao, exibir_erros, pesquisa, resultado_pesquisa 

def operacao_rotas(app):
    app.add_url_rule("/operacoes", endpoint="listar_todas_operacoes", view_func=listar_todas_operacoes, methods=['GET'])
    app.add_url_rule("/operacoes/nova", endpoint="cadastrar_operacao", view_func=cadastrar_operacao, methods=['GET', 'POST'])
    app.add_url_rule("/operacoes/<id>", endpoint="visualizar_operacao", view_func=visualizar_operacao, methods=['GET'])
    app.add_url_rule("/operacoes/<id>/editar", endpoint="editar_operacao", view_func=editar_operacao, methods=['GET', 'POST'])
    app.add_url_rule("/operacoes/<id>/apagar", endpoint="apagar_operacao", view_func=apagar_operacao, methods=['POST'])
    app.add_url_rule("/erros", endpoint="exibir_erros", view_func=exibir_erros, methods=['POST'])
    app.add_url_rule("/pesquisa", endpoint="pesquisa", view_func=pesquisa, methods=['GET'])
    app.add_url_rule('/resultado_pesquisa', view_func=resultado_pesquisa, methods=['GET'])

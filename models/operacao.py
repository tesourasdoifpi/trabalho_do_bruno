from daos.operacao_dao import OperacaoDAO
import random
from utils.validacao import codigo_valido, data_valida



class Operacao:
    TIPO_OPERACAO = {1: "Compra", 2: "Venda"}

    def __init__(self, dados):
        self._dados = dict(dados) if dados else {}
        self.errors = []

        if not self._dados.get("id"):
            self._dados["id"] = self._gerar_id()

        quantidade = self._dados.get("quantidade")
        valor_unitario = self._dados.get("valor_unitario")

        if quantidade is not None and valor_unitario is not None:
            try:
                # Garante cálculo seguro e arredondado para 2 casas decimais
                bruto = float(quantidade * valor_unitario)
                self._dados["valor_bruto"] = round(bruto, 2)
            except (TypeError, ValueError):
                self._dados["valor_bruto"] = 0.0

        # Taxas correspondem a 0,03% (0.0003) do valor bruto
        valor_bruto = self._dados.get("valor_bruto", 0.0)
        taxas = round(valor_bruto * 0.0003, 2)
        self._dados["taxas"] = taxas

        tipo_operacao = self._dados.get("tipo_operacao")
        if tipo_operacao == 1:  # Compra: valor_bruto + taxas
            self._dados["valor_liquido"] = round(valor_bruto + taxas, 2)
        elif tipo_operacao == 2:  # Venda: valor_bruto - taxas
            self._dados["valor_liquido"] = round(valor_bruto - taxas, 2)

    def validate(self):
        self.errors = []

        data = self._dados.get("data")
        if not data:
            self.errors.append("A operação deve conter uma data")

        # No modelo, o código do ativo é representado pelo atributo 'ativo'
        codigo = self._dados.get("ativo") or self._dados.get("codigo")
        if not codigo:
            self.errors.append("A operação precisa de um código de ativo")
        elif not codigo_valido(codigo):
            self.errors.append(
                "O código da operação tem que ser composto por quatro letras"
                " maiúsculas seguidas de um ou dois números"
            )

        quantidade = self._dados.get("quantidade")
        if quantidade is None:
            self.errors.append("A operação precisa de uma quantidade")
        elif not isinstance(quantidade, int) or quantidade <= 0:
            self.errors.append(
                "A quantidade da operação precisa ser um número inteiro positivo."
            )

        valor_unitario = self._dados.get("valor_unitario")
        if valor_unitario is None:
            self.errors.append("A operação precisa de um valor unitário")
        elif not isinstance(valor_unitario, (int, float)) or valor_unitario <= 0:
            self.errors.append("O valor unitário precisa ser monetário e positivo.")

        tipo_operacao = self._dados.get("tipo_operacao")
        if tipo_operacao not in self.TIPO_OPERACAO:
            self.errors.append("Tipo de operação inválida!")

        return len(self.errors) == 0

    @staticmethod
    def pegar_por_id(id):
        dao = OperacaoDAO()
        return dao.buscar_operacao_por_id(id)

    def atualizar(self):
        """Atualiza os dados da operação existente no banco de dados."""
        if self.validate():
            dao = OperacaoDAO()
            return dao.atualizar_operacao(self.id, self._dados)
        return False

    def apagar(self):
        """Remove a operação atual do banco de dados."""
        if self.id:
            dao = OperacaoDAO()
            return dao.deletar_operacao(self.id)
        return False

    @staticmethod
    def pesquisa_por_data(data_inicio, data_fim):
        dao = OperacaoDAO()
        return dao.pesquisar_por_periodo(data_inicio, data_fim)

    @staticmethod
    def pesquisa_por_termo(termo):
        dao = OperacaoDAO()
        return dao.pesquisa_por_id_e_ativo(termo)

    def save(self):
        """Salva uma nova operação no banco de dados se os dados forem válidos."""
        if self.validate():
            dao = OperacaoDAO()
            return dao.nova_operacao(self._dados)
        return False

    @staticmethod
    def get_operacoes():
        """Retorna uma lista com todas as operações cadastradas."""
        dao = OperacaoDAO()
        return dao.listar_operacoes()

    @classmethod
    def _gerar_id(cls):
        while True:
            novo_id = random.randint(1000000000, 9999999999)
            if not cls.pegar_por_id(novo_id):
                return novo_id


    @property
    def id(self):
        return self._dados.get("id")

    @property
    def data(self):
        return self._dados.get("data")

    @property
    def data_formatada(self):
        valor = self._dados.get("data")
        
        if not valor:
            return None
            
        # Se o conector do banco já converteu para datetime.date
        if hasattr(valor, 'strftime'):
            return valor.strftime("%d/%m/%Y")
            
        # Se o banco entregou como string "YYYY-MM-DD" (comum no SQLite)
        if isinstance(valor, str):
            ano, mes, dia = valor.split("-")
            return f"{dia}/{mes}/{ano}"
            
        return valor

    @property
    def ativo(self):
        return self._dados.get("ativo") or self._dados.get("codigo")

    @property
    def quantidade(self):
        return self._dados.get("quantidade")

    @property
    def valor_unitario(self):
        return self._dados.get("valor_unitario")

    @property
    def tipo_operacao(self):
        return self._dados.get("tipo_operacao")

    @property
    def valor_bruto(self):
        return self._dados.get("valor_bruto")

    @property
    def taxas(self):
        return self._dados.get("taxas")

    @property
    def valor_liquido(self):
        return self._dados.get("valor_liquido")
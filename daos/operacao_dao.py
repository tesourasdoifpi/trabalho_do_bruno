from databases.sqlitedb import SQLiteDB

class OperacaoDAO:
    def __init__(self):
        self.db = SQLiteDB()

    
    @staticmethod
    def formatar_data(data_origem):
        """Converte uma data do banco (objeto date ou string AAAA-MM-DD) para DD/MM/YYYY"""
        if not data_origem:
            return None
            
        # Se o banco retornou um objeto date/datetime nativo
        if hasattr(data_origem, 'strftime'):
            return data_origem.strftime("%d/%m/%Y")
            
        # Se o banco retornou uma string (ex: SQLite)
        if isinstance(data_origem, str) and "-" in data_origem:
            # O split(" ")[0] previne erros caso a string venha com horário (AAAA-MM-DD HH:MM:SS)
            data_apenas = data_origem.split(" ")[0] 
            ano, mes, dia = data_apenas.split("-")
            return f"{dia}/{mes}/{ano}"
            
        # Retorna o valor original caso não caia em nenhuma das opções
        return data_origem

    def nova_operacao(self, dado: dict):
        self.db.conectar()
        try:
            sql = """
                INSERT INTO operacoes (id, data, ativo, quantidade, valor_unitario, tipo_operacao, valor_bruto, taxas, valor_liquido) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
            params = (
                dado.get("id"),
                dado.get("data"),
                dado.get("ativo"),
                dado.get("quantidade"),
                dado.get("valor_unitario"),
                dado.get("tipo_operacao"),
                dado.get("valor_bruto"),
                dado.get("taxas"),
                dado.get("valor_liquido")
            )
            resultado = self.db.executar(query=sql, params=params)
            return resultado
        finally:
            self.db.desconectar()

    def listar_operacoes(self):
        self.db.conectar()
        try:
            sql = "SELECT id, data, ativo, quantidade, valor_unitario, tipo_operacao, valor_bruto, taxas, valor_liquido FROM operacoes;"
            resultados = self.db.consultar(query=sql)
            
            operacoes = []
            for row in resultados:
                dados = {                
                    "id": row["id"],
                    "data": self.formatar_data(row["data"]),
                    "ativo": row["ativo"],
                    "quantidade": row["quantidade"],
                    "valor_unitario": row["valor_unitario"],
                    "tipo_operacao": row["tipo_operacao"],
                    "valor_bruto": row["valor_bruto"],
                    "taxas": row["taxas"],
                    "valor_liquido": row["valor_liquido"]
                }
                operacoes.append(dados)
                
            return operacoes # Movido para fora do loop!
        finally:
            self.db.desconectar()

    def buscar_operacao_por_id(self, id):
        self.db.conectar()
        try:
            sql = "SELECT id, data, ativo, quantidade, valor_unitario, tipo_operacao, valor_bruto, taxas, valor_liquido FROM operacoes WHERE id = ?;"
            resultado = self.db.consultar(query=sql, params=(id,))
            
            if resultado and len(resultado) > 0:
                row = resultado[0]
                return {
                    "id": row["id"],
                    "data": row["data"],
                    "ativo": row["ativo"],
                    "quantidade": row["quantidade"],
                    "valor_unitario": row["valor_unitario"],
                    "tipo_operacao": row["tipo_operacao"],
                    "valor_bruto": row["valor_bruto"],
                    "taxas": row["taxas"],
                    "valor_liquido": row["valor_liquido"]
                }
            return None
        finally:
            self.db.desconectar()


    def atualizar_operacao(self, id, dado: dict):
        """Atualiza os dados de uma operação existente com base no ID."""
        self.db.conectar()
        try:
            sql = """
                UPDATE operacoes 
                SET data = ?, 
                    ativo = ?, 
                    quantidade = ?, 
                    valor_unitario = ?, 
                    tipo_operacao = ?, 
                    valor_bruto = ?, 
                    taxas = ?, 
                    valor_liquido = ? 
                WHERE id = ?;
            """
            params = (
                dado.get("data"),
                dado.get("ativo"),
                dado.get("quantidade"),
                dado.get("valor_unitario"),
                dado.get("tipo_operacao"),
                dado.get("valor_bruto"),
                dado.get("taxas"),
                dado.get("valor_liquido"),
                id
            )
            resultado = self.db.executar(query=sql, params=params)
            return resultado
        finally:
            self.db.desconectar()

    def deletar_operacao(self, id):
        """Remove uma operação do banco de dados com base no ID."""
        self.db.conectar()
        try:
            sql = "DELETE FROM operacoes WHERE id = ?;"
            resultado = self.db.executar(query=sql, params=(id,))
            return resultado
        finally:
            self.db.desconectar()       


    def pesquisa_por_id_e_ativo(self, termo):
        self.db.conectar()

        try:
            termo_like = f"%{str(termo).upper()}%"
           
            sql = """
                SELECT id, data, ativo, quantidade, valor_unitario, tipo_operacao, 
                    valor_bruto, taxas, valor_liquido 
                FROM operacoes 
                WHERE CAST(id AS TEXT) LIKE ? 
                OR UPPER(ativo) LIKE ?;
            """
            
            resultados = self.db.consultar(query=sql, params=(termo_like, termo_like))
            
            operacoes = []
            for row in resultados:
                dados = {                
                    "id": row["id"],
                    "data": self.formatar_data(row["data"]), 
                    "ativo": row["ativo"],
                    "quantidade": row["quantidade"],
                    "valor_unitario": row["valor_unitario"],
                    "tipo_operacao": row["tipo_operacao"],
                    "valor_bruto": row["valor_bruto"],
                    "taxas": row["taxas"],
                    "valor_liquido": row["valor_liquido"]
                }
                operacoes.append(dados)
                
            return operacoes
            
        finally:
            self.db.desconectar()


    def pesquisar_por_periodo(self, data_inicio, data_fim):

        self.db.conectar()
        try:
     
            sql = """
                SELECT id, data, ativo, quantidade, valor_unitario, tipo_operacao, 
                       valor_bruto, taxas, valor_liquido 
                FROM operacoes 
                WHERE data BETWEEN ? AND ?
                ORDER BY data ASC;
            """
            
            
            resultados = self.db.consultar(query=sql, params=(data_inicio, data_fim))
            
            operacoes = []
            for row in resultados:
                dados = {                
                    "id": row["id"],
                    "data": self.formatar_data(row["data"]), 
                    "ativo": row["ativo"],
                    "quantidade": row["quantidade"],
                    "valor_unitario": row["valor_unitario"],
                    "tipo_operacao": row["tipo_operacao"],
                    "valor_bruto": row["valor_bruto"],
                    "taxas": row["taxas"],
                    "valor_liquido": row["valor_liquido"]
                }
                operacoes.append(dados)
                
            return operacoes
            
        finally:
            self.db.desconectar()
import sqlite3

class SQLiteDB:
    DB_FILE = "banco.db"

    def __init__(self):
        self.db_name = self.DB_FILE
        self.conn = None
        self.cursor = None


    def conectar(self):
        """Abre a conexão com o banco de dados."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Erro ao conectar: {e}")
            self.conn = None
            self.cursor = None

    def desconectar(self):
        """Fecha a conexão com o banco de dados."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def executar(self, query, params=()):
        """Executa comandos INSERT, UPDATE, DELETE com commit."""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.rowcount  # Retorna o número de linhas afetadas 
        except sqlite3.Error as e:
            self.cursor.rollback()  # Desfaz as alterações em caso de erro
            print(f"Erro ao executar: {e}")
            return 0

    def consultar(self, query, params=()):
        """Executa consultas SELECT e retorna os resultados."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao consultar: {e}")
            return None
    
    def executar_script_sql(self, sql_file):
        """Executa um arquivo SQL em um banco de dados SQLite."""
        with open(sql_file, 'r', encoding='utf-8') as f:
            script_sql = f.read()
        try:
            self.cursor.executescript(script_sql)
            self.conn.commit() # Salva as alterações
            print("Script executado com sucesso!")
        except sqlite3.Error as e:
            self.cursor.rowback()  # Desfaz as alterações em caso de erro
            print(f"Erro ao executar o script: {e}")
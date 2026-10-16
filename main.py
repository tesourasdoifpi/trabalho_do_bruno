from flask import Flask
from databases.sqlitedb import SQLiteDB
from routers.operacao_router import operacao_rotas

app = Flask(__name__)

db = SQLiteDB()
db.conectar()
db.executar_script_sql('databases/scripts/criar_tabela.sql')


operacao_rotas(app)
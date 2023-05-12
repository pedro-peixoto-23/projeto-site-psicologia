import sqlite3 as sql

# conectando-se com o banco de dados
conexao_banco_dados = sql.connect('agendamentos.db')
conexao_banco_dados.execute(
    'CREATE TABLE IF NOT EXISTS agendamentos (id integer primary key autoincrement, nome text, cpf text, email text, horario text, servico text)')
conexao_banco_dados.close()

import sqlite3 as sql

conexao = sql.connect('database-cadastrados-banco-dados.db')
conexao.execute('CREATE TABLE IF NOT EXISTS cadastrados (id integer primary key autoincrement, nome_usuario text, senha text)')
conexao.close()
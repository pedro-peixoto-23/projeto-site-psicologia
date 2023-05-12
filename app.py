# Autor do código: Pedro Peixoto Viana de Oliveira.


"""

    Sobre o projeto:

        Objetivo principal: 
            Criar um site, para uma Clínica de Psicologia, responsável por disponibilizar ao usuário a visão
            geral da clínica, fornecer a possibilidade de realizar agendamentos de consultas, visualizar os
            dados das consultas já agendadas, permitir ele apagar a consulta que já foi realizada.

            Além disso, é necessário ter a parte dos "funcionários" responsáveis por gerenciar os agendamentos,
            podendo apagar uma consulta se necessário, e isso será acessado através de um login.

            Fora isso, é imprescindível que haja um outro banco de dados com os dados das pessoas com permissão
            para acessar o banco de dados com os agendamentos. Isso será feito pelo "gerente", que irá fazer
            os cadastros das pessoas que terão permissão de acessar os agendamentos, assim como apagar quem desejar
        

        Esse projeto é composto por três áreas: área do usuário, área de acesso ao banco de dados com os agendamentos 
        e área de gerenciamento de acessso das pessoas que podem acessar o banco de dados.

            -   Área do usuário: aqui é onde o usuário pode ver sobre a Clínica, realizar um agendamento de consulta, ver 
                os dados de um agendamento que já foi realizado. 
            -   Área de acesso aos agendamentos: o usuário não tem acesso a essa parte, é o local onde é possível acessar
                o banco de dados com todos os agendamentos e tem a possibilidade de excluir um agendamento.
            -   Área de gerenciamento das pessoas que podem acessar o banco de dados com os agendamentos: aqui é o local
                que o "gerente fictício" vai cadastrar novas pessoas que podem acessar o banco de agendamentos, assim
                como excluir pessoas.
            
            Acesso (Área do usuário) -> é feito através da navegação do site principal.
            Acesso (Áre de acesso aos agendamentos) -> é feito através da rota: \agendamentos, mas, caso a pessoa não tenha
                                                       feito o login anteriormente, é direcionada para a página de login.
            Acesso (Área de gerenciamento do acesso aos agendamentos) -> é feito através da rota: /pessoas-permitidas-usar-banco-dados
                                                                         em teoria, apenas o "gerente fictício" tem ciência dessa rota.

"""

"""

    Necessário para rodar esse código:

        - Bibliotecas (não precisa instalar essa biblioteca, pois está no ambiente virtual "env"):
            - Flask: pip install flask

        - Ativar o ambiente virtual "env"
            - Cmd do Windows: .\env\Scripts\Activate.bat
            - Powershel do Windows: .\env\Scripts\Activate.ps1
                - Caso haja um erro, inserir esse código no PowerShell: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
        
        - Acessar o arquivo: .\app.py

        - Copiar o link do servidor flask gerado e inserir no seu navegador
    
    Bibliotecas utilizadas: flask e sqlite3

"""

# Sobre os dois bancos de dados: "agendamentos.db" (responsável por armazenar os agendamentos) e 
# "database-cadastrados-banco-dados" (responsável por armazenar o login das pessoas com permissão
# para acessar o banco de dados com as consultas marcadas).

# Visão geral da utilização de cada função da biblioteca flask que foi utilizada no código:
#       render_template: necessário para retornar arquivos html para o usuário
#       request: necessário para receber os dados dos formulários
#       redirect: necessário para redirecionar para outra rota
#       session: necessário para criar uma sessão para o usuário, e deixar ele acessar uma rota 
#                apenas se ele estiver na sessão


from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # necessário para criptografar os dados dos coockies da sessão


# 1. Funcionalidades do usuário que irá acessar o site

# Rota responsável por retornar o html com a tela inicial
@app.route('/')
def tela_inicial():
    return render_template('/principais/tela_inicial.html')


# Retorna o html com as especificações da clínica, mostrando como ela trabalha
@app.route('/especificacoes')
def especificacoes():
    return render_template('/principais/especificacoes.html')


# Essa rota retorna o html com o formulário de agendamento
@app.route('/marcar_consulta')
def marcar_consulta():
    return render_template('/principais/marcar_consulta.html')


# Essa rota tem a função de receber os dados do formulário de agendamento e verificar se já
# existe alguma consulta já agendada com o cpf inserido pelo usuário, caso exista, retorna
# o html de erro, informando que já foi feito um agendamento com o cpf digitado. Caso não exista,
# insere os dados informados para o agendamento no banco de dados de agendamento e retorna o html
# com a mensagem de consulta agendada com sucesso.
@app.route("/receber_dados", methods=['POST'])
def receber_dados():
    cpf_usuario = request.form['cpf']

    conexao_banco_dados = sql.connect('agendamentos.db')
    cursor = conexao_banco_dados.cursor()
    cursor.execute(
        "SELECT cpf FROM agendamentos WHERE cpf = ?", (cpf_usuario,))

    linhas = cursor.fetchall()

    if len(linhas) == 0:
        with sql.connect('agendamentos.db') as conexao:
            cursor = conexao.cursor()
            cursor.execute('INSERT INTO agendamentos (nome, cpf, email, horario, servico) VALUES (?,?,?,?,?)', (
                request.form['nome'], request.form['cpf'], request.form['email'], request.form['horario'], request.form['servico']))
            conexao.commit()
        return redirect('/consulta_agendada')

    else:
        conexao_banco_dados.commit()
        return render_template('/telas-finalizacao-e-erro/erro_ja_tem_agendamento.html')


# Retorna um html informando que a consulta foi agendada com sucesso
@app.route('/consulta_agendada')
def consulta_agendada():
    return render_template('/telas-finalizacao-e-erro/consulta_agendada.html')


# Retorna o html com o formulário que recebe o cpf para verificar os dados de agendamento
@app.route('/verificar_dados_agendamento')
def verificar_dados_agendamento():
    return render_template('/principais/verificar_dados_agendamento.html')


# Essa rota é responsável por verificar o cpf informado no formulário de verificação de dados de
# agendamento e verificar se ele existe no banco de dados, se existir, retorna o html com as informações
# do agendamento. Caso não exista, retorna um html informando que não existe no banco de dados o cpf
# informado.
# Além disso, ele cria uma variável cpf global para que possa ser acessado enquanto ele estiver
# na página html que mostra os dados da consulta, pois será necessário caso ele queira apagar
# a consulta.
@app.route('/receber_cpf_verificacao', methods=['POST'])
def receber_cpf_verificacao():
    global cpf_usuario_verificar_consulta
    cpf_usuario_verificar_consulta = request.form['cpf']

    conexao_banco_dados = sql.connect('agendamentos.db')
    cursor = conexao_banco_dados.cursor()
    cursor.execute("SELECT * FROM agendamentos WHERE cpf = ?",
                   (cpf_usuario_verificar_consulta,))
    linhas = cursor.fetchall()
    conexao_banco_dados.commit()

    if len(linhas) == 0:
        return render_template('/telas-agendado-nao-agendado/nao_agendado.html')
    else:
        return render_template('/telas-agendado-nao-agendado/ja_agendado.html', consulta_cadastrada=linhas)


# Essa rota chama a função que retorna um html que pergunta ao usuário se ele deseja realmente apagar
# o agendamento.
@app.route('/verificar_se_quer_apagar')
def verificar_se_quer_apagar():
    return render_template('/telas-finalizacao-e-erro/apagar_ou_nao.html')


# Essa rota chama a função que apaga o agendamento usando a variável global do cpf criada na rota
# /receber_cpf_verificacao e redireciona para a rota que mostra o html informando que o agendamento
# foi apagado com sucesso.
@app.route('/apagar_consulta')
def apagar_consulta():
    agendamento_para_apagar = cpf_usuario_verificar_consulta

    with sql.connect('agendamentos.db') as conexao_banco_dados:
        cursor = conexao_banco_dados.cursor()
        cursor.execute('DELETE FROM agendamentos WHERE cpf = ?',
                       (agendamento_para_apagar,))
        conexao_banco_dados.commit()

    return redirect('/consulta_apagada')


# Essa rota retorna o html que mostra que o agendamento foi apagado com sucesso
@app.route('/consulta_apagada')
def consulta_apagada():
    return render_template('/telas-finalizacao-e-erro/consulta_apagada.html')


# 2. Funcionalidades do banco de dados dos cadastrados para mexer no banco de dados de agendamentos

# Essa rota é responsável por retornar um html com todos os agendamentos. Mas não é possível 
# acessar essa rota caso não tenha feito o login na sessão. E caso isso aconteça, redireciona
# para a rota a seguir, que pede o login no banco de dados. Caso já tenha feito o login, retorna
# o html com os agendamentos e também manda para esse html o usuário que está logado, para que
# o usuário veja que está logado na conta.
@app.route('/agendamentos')
def agendamentos():
    if 'usuario' in session:
        conexao_banco_dados = sql.connect('agendamentos.db')
        conexao_banco_dados.row_factory = sql.Row

        cursor = conexao_banco_dados.cursor()
        cursor.execute(
            'SELECT id, nome, cpf, email, horario, servico FROM agendamentos')
        linhas = cursor.fetchall()
        conexao_banco_dados.commit()
        return render_template('agendamentos.html', dados=linhas, usuario_dentro=session['usuario'])
    else:
        return redirect('/login-banco-dados')


# Essa rota retorna o html de login para acessar os dados dos agendamentos. 
@app.route('/login-banco-dados')
def login_banco_dados():
    return render_template('/banco-dados-acesso/login-banco-dados.html')


# Essa rota é responsável por verificar se os dados de login inseridos na rota anterior são válidos
# ou seja, ele só vai ser redirecionado para o banco com os agendamentos se o login e senha estiver
# no banco de dados de pessoas com permissão para acessar o banco de dados. Caso o login não seja
# bem sucessido, retorna um alerta mostrando que os dados inseridos não são válidos
@app.route('/verificar_login', methods=['POST'])
def verificar_login():
    login = request.form['login']
    senha = request.form['senha']

    conexao_banco_dados = sql.connect('database-cadastrados-banco-dados.db')
    cursor = conexao_banco_dados.cursor()
    cursor.execute(
        "SELECT nome_usuario FROM cadastrados WHERE nome_usuario = ? AND senha = ?", (login, senha,))

    linhas = cursor.fetchall()

    if len(linhas) == 0:
        return render_template('/banco-dados-acesso/login-banco-dados.html', sucesso=False)
    else:
        session['usuario'] = login
        session['senha'] = senha
        return redirect('/agendamentos')
    # return render_template('/banco-dados-acesso/login-banco-dados.html')


# Essa rota é chamada quando é apertado o botão de deletar na lista de agendamentos, e vai com
# ele o id da linha que deseja deletar, desta forma, ela apenas tem a função de verificar no banco de 
# dados qual o agendamento que tem esse id e deleta essa linha da tabela. E redireciona novamente
# para a rota de agendamentos.
@app.route('/agendamentos/apagar/<int:id>')
def apagar_agendamento_por_botao_banco_dados(id):
    with sql.connect('agendamentos.db') as conexao_banco_dados:
        cursor = conexao_banco_dados.cursor()
        cursor.execute('DELETE FROM agendamentos WHERE id = ?', (str(id),))
        conexao_banco_dados.commit()
    return redirect('/agendamentos')


# 3. Funcionalidades para cadastrar novas pessoas que tem acesso ao banco de dados

# Essa rota retorna um arquivo html com uma lista com todas as pessoas permitidas para 
# acessarem o banco de dados com os agendamentos
@app.route('/pessoas-permitidas-usar-banco-dados')
def pessoas_permitidas():
    conexao_banco_dados = sql.connect('database-cadastrados-banco-dados.db')
    conexao_banco_dados.row_factory = sql.Row

    cursor = conexao_banco_dados.cursor()
    cursor.execute(
        'SELECT id, nome_usuario, senha FROM cadastrados')
    linhas = cursor.fetchall()
    conexao_banco_dados.commit()
    return render_template('/banco-dados-acesso/pessoas_permitidas.html', dados=linhas)


# Essa rota retorna o html com o formulário de cadastro de novas pessoas que podem
# acessar o banco de dados dos agendamentos
@app.route('/pessoas-permitidas-usar-banco-dados/cadastro')
def cadastro_pessoas_permitidas():
    return render_template('/banco-dados-acesso/cadastrar-pessoa.html')


# Essa rota é responsável por pegar os dados inseridos na rota anterior, verificar se já existe
# no banco de dados e, se não existir, insere no banco de dados a nova pessoa que pode acessar
# o banco de dados com os agendamentos
@app.route('/pessoas-permitidas-usar-banco-dados/novo', methods=['POST'])
def inserindo_banco_dados_nova_pessoa():
    login = request.form['login']
    senha = request.form['senha']

    conexao_banco_dados = sql.connect('database-cadastrados-banco-dados.db')
    cursor = conexao_banco_dados.cursor()
    cursor.execute(
        "SELECT nome_usuario FROM cadastrados WHERE nome_usuario = ? AND senha = ?", (login, senha,))

    linhas = cursor.fetchall()

    if len(linhas) == 0:
        with sql.connect('database-cadastrados-banco-dados.db') as conexao:
            cursor = conexao.cursor()
            cursor.execute('INSERT INTO cadastrados (nome_usuario, senha) VALUES (?,?)', (
                request.form['login'], request.form['senha']))
            conexao.commit()
        return redirect('/pessoas-permitidas-usar-banco-dados')

    else:
        conexao_banco_dados.commit()
        return render_template('/banco-dados-acesso/pessoas_permitidas.html')


# Essa rota traz consigo uma variável "id" quem vem da página html "pessoas_permitidas.html" e
# essa rota é responsável por pegar esse "id", procurar no banco quem tem esse id e deletar ele
# e retorna para a página novamente de listagem com as pessoas permitidas.
@app.route('/pessoas-permitidas-usar-banco-dados/apagar/<int:id>')
def apagar_pessoas_permitidas(id):
    with sql.connect('database-cadastrados-banco-dados.db') as conexao_banco_dados:
        cursor = conexao_banco_dados.cursor()
        cursor.execute('DELETE FROM cadastrados WHERE id = ?', (str(id),))
        conexao_banco_dados.commit()
    return redirect('/pessoas-permitidas-usar-banco-dados')


# Inicia a aplicação
if __name__ == "__main__":
    app.run()

# Projeto - Site para Clínica de Psicologia

# Descrição do projeto
O objetivo do projeto é criar um site para uma Clínica de Psicologia, onde o usuário possa conhecer a clínica, realizar agendamento de consulta, ver os dados de agendamento de uma consulta já realizada e apagar um agendamento caso necessário.

Além disso, é necessário ter o acesso aos agendamentos e apagar alguns, se necessário, por parte dos "funcionários". Para isso, terá um login para ter acesso a essa lista de consultas marcadas.

Quem realiza o cadastro de novos "funcionários" é o "gerente", que tem acesso a rota com a lista de pessoas com permissão para acessar os agendamentos, além de poder inserir novas pessoas com permissão, assim como excluir.

Esse é o funcionamento básico do projeto.


# Tecnologias utilizadas
FrontEnd: HTML5 e CSS3 simples

Backend: Python, mini Framework Flask, biblioteca sql3 para o banco de dados.

## Observações
### Como rodar o projeto?
#### Para rodar o programa, basta seguir os seguintes passos:

- Baixar os arquivos do projeto
- Bibliotecas (não precisa instalar essa biblioteca, pois está no ambiente virtual "env"):
    - Flask: pip install flask
- Ativar o ambiente virtual "env"
    - Cmd do Windows: .\env\Scripts\Activate.bat
    - Powershel do Windows: .\env\Scripts\Activate.ps1
        - Caso haja um erro, inserir esse código no PowerShell: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

- Acessar o arquivo: .\app.py

- Copiar o link do servidor flask gerado e inserir no seu navegador
- Pronto! Já é possível acessar as rotas do flask (no arquivo "app.py" é abordado como funciona o código)

### Informações extras
- Página inicial para o usuário: link dado pelo flask ao executar o arquivo python
- Rota para lista das pessoas com acesso ao banco de dados de agendamentos: "/pessoas-permitidas-usar-banco-dados"
- Rota para acessar o banco de dados com os agendamentos: "\agendamentos"

- Para finalizar a execução do código, digite:  ctrl + c


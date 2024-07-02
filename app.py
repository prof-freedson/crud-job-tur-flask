# Importação dos pacotes
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import re
import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())

host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
database = os.getenv("database")

# Herdando a classe Flask
app = Flask(__name__)


# Configuração do banco de dados
# Verificando a conexão

try:
    conexao = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if conexao.is_connected():
        print('Conexão realizada com sucesso')
except OSError as error:
    print('Erro ao conectar: ', error)

# Herdando o método de execução
# dos scripts em SQL
cursor = conexao.cursor(dictionary=True)


# criação das rotas para o
# carregamento das páginas e
# realização das operações CRUD


# 1) Rota para acesso
# da página principal da aplicação
@app.route('/')
def index():
    return render_template('index.html')


# 2) Rota para criação de
# registros no banco
@app.route('/criar', methods=['GET', 'POST'])
def criar():

    # Verificar qual método será
    # usado na operação e atribuir
    # variáveis para receber os valores
    # dos campos de texto(inputs)
    if request.method == 'POST':
        sexo = request.form['sexo']
        nome_passageiro = request.form['nome_passageiro']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        cidade_partida = request.form['cidade_partida']
        cidade_destino = request.form['cidade_destino']
        preco = request.form['preco']

        # Comando em SQL para criar
        # o paciente
        comando = 'insert into viagem(sexo, nome_passageiro, endereco, telefone, cidade_partida, cidade_destino, preco) values(%s, %s, %s, %s, %s, %s, %s)'

        # Variável que irá receber todos
        # os valores das variáveis anteriores
        valores = (sexo, nome_passageiro, endereco, telefone,
                   cidade_partida, cidade_destino, preco)

        # Executar o comando em SQL
        cursor.execute(comando, valores)

        # Confirmar a execução do
        # comando no banco de dados
        conexao.commit()

        # Atribuir um retorno podendo
        # ser o redirecionamento para
        # outra página
        return redirect(url_for('listar'))
        # OBS: o parâmetro em 'url_for'
        # é a função criada para
        # carregar a rota desejada

    # Atribuir um retorno para o
    # carregamento da página de
    # de criação do paciente
    return render_template('criar.html')


# Função para buscar os
# valores declarados em
# uma coluna do tipo 'enum'
def enum_sexo():
    # Script para selecionar
    # os valores de uma coluna
    # com tipo 'enum'
    comando = "show columns from viagem like 'sexo'"
    cursor.execute(comando)
    resultado = cursor.fetchone()
    print(resultado)
    # Buscar os valores em um dicionário
    # com a chave chamada 'Type'
    enum_resultado = resultado['Type']
    # Filtrar somente o nome dos valores
    enum_valores = re.findall(r"'(.*?)'", enum_resultado.decode('utf-8'))
    return enum_valores


# 3) Rota para seleção de
# registros no banco
@app.route('/listar')
def listar():
    # Comando em SQl para selecionar
    # os pacientes
    comando = 'select * from viagem'

    # Executar o comando em SQL
    cursor.execute(comando)

    # Variável que irá receber
    # o resultado do comando
    viagens = cursor.fetchall()

    # retornar o resultado
    # carregando em outra página
    return render_template('listar.html', viagens=viagens)
    # A primeira variável 'viagens' recebe o resultado
    # da execução do comando em SQL

    # A segunda variável 'viagens' é um apelido
    # atribuído para ser carregado na página e
    # realizar estruturas de programação


@app.route('/visualizar/<int:id_viagem>')
def visualizar(id_viagem):
    comando = 'select * from viagem where id_viagem = %s'
    valor = (id_viagem,)
    cursor.execute(comando, valor)
    viagem = cursor.fetchone()
    return render_template('ver.html', viagem=viagem)


# 4) Rota para atualização de
# registros no banco
@app.route('/editar/<int:id_viagem>', methods=['GET', 'POST'])
def editar(id_viagem):
    if request.method == 'POST':
        sexo = request.form['sexo']
        nome_passageiro = request.form['nome_passageiro']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        cidade_partida = request.form['cidade_partida']
        cidade_destino = request.form['cidade_destino']
        preco = request.form['preco']

        comando = 'update viagem set sexo = %s, nome_passageiro = %s, endereco = %s, telefone = %s, cidade_partida = %s, cidade_destino = %s, preco = %s where id_viagem = %s'

        valores = (sexo, nome_passageiro, endereco, telefone,
                   cidade_partida, cidade_destino, preco, id_viagem)

        cursor.execute(comando, valores)

        conexao.commit()

        return redirect(url_for('listar'))

    # ====== PRIMEIRO PASSO ==========
    # Comando SQL para selecionar
    # somente um paciente pelo id

    # Chamando a função que
    # seleciona os valores
    # do tipo 'enum' da coluna sexo
    opcoes = enum_sexo()

    comando = 'select * from viagem where id_viagem = %s'

    # Variável que irá receber
    # o valor do id do paciente
    valor = (id_viagem,)

    # Executar o comando em SQL
    cursor.execute(comando, valor)

    # Atribuir um retorno para o
    # carregamento da página de
    # de criação do viagem e atribuir
    # um apelido
    viagem = cursor.fetchone()

    # retornar o resultado
    # carregando em outra página

    # OBS: atribuir o resultado com
    # um apelido para buscar os valores
    # do tipo 'enum' para a coluna sexo
    return render_template('editar.html', viagem=viagem, opcoes=opcoes)

    # ====== SEGUNDO PASSO ==========

    # Verificar qual método será
    # usado na operação e atribuir
    # variáveis para receber os valores
    # dos campos de texto(inputs)

    # Comando em SQl para editar
    # o paciente

    # Variável que irá receber todos
    # os valores das variáveis anteriores

    # Executar o comando em SQL

    # Atribuir um retorno podendo
    # ser o redirecionamento para
    # outra página


# 5) Rota para exclusão de
# registros no banco
@app.route('/excluir/<int:id_viagem>')
def excluir(id_viagem):
    # Comando em SQl para excluir
    # a viagem
    comando = 'delete from viagem where id_viagem = %s'

    # Variável que irá receber
    # o valor do id da viagem
    valor = (id_viagem,)

    # Executar o comando em SQL
    cursor.execute(comando, valor)

    # Confirmar a execução do
    # comando no banco de dados
    conexao.commit()

    # Atribuir um retorno podendo
    # ser o redirecionamento para
    # outra página
    return redirect(url_for('listar'))


# Inicialização do servidor
if __name__ == '__main__':
    app.run(debug=True)

import sqlite3
import os


# Função para conectar ao banco de dados ou criá-lo se não existir
def connect():
    # Conecta ao banco de dados 'banco_de_dados.db' ou o cria se não existir
    conn = sqlite3.connect("banco_de_dados.db")
    # Cria um cursor para executar comandos SQL
    cur = conn.cursor()
    # Cria a tabela 'banco_de_dados' se ainda não existir
    cur.execute(
        "CREATE TABLE IF NOT EXISTS banco_de_dados (id INTEGER PRIMARY KEY,"
        " titulo text, plataforma text, estoque integer,valor float, codigo integer )")
    # executa o commit do banco de dados para confirmar as alterações e fecha a conexão
    conn.commit()
    conn.close()


# Função para inserir um novo registro no banco de dados
def insert(titulo, plataforma, estoque, valor, codigo):
    conn = sqlite3.connect("banco_de_dados.db")
    cur = conn.cursor()
    # Insere os dados na tabela 'banco_de_dados'
    cur.execute("INSERT INTO banco_de_dados VALUES (NULL,?,?,?,?,?)",
                (titulo, plataforma, estoque, valor, codigo))
    conn.commit()
    conn.close()


# Função para recuperar todos os registros da tabela 'banco_de_dados'
def view():
    conn = sqlite3.connect("banco_de_dados.db")
    cur = conn.cursor()
    # Executa a consulta SQL para recuperar todos os registros
    cur.execute("SELECT * FROM banco_de_dados")
    # Recupera todos os registros
    rows = cur.fetchall()
    conn.close()
    # Retorna os registros recuperados
    return rows


# Função de busca de registros com base em critérios específicos
def search(titulo="", plataforma="", estoque="", valor="", codigo=""):
    conn = sqlite3.connect("banco_de_dados.db")
    cur = conn.cursor()
    # Executa a consulta SQL com base nos critérios fornecidos
    cur.execute("SELECT * FROM banco_de_dados WHERE titulo=? OR plataforma=? OR estoque=? OR valor=? OR codigo=?",
                (titulo, plataforma, estoque, valor, codigo))
    # Recupera os registros que correspondem aos critérios
    rows = cur.fetchall()
    conn.close()
    # Retorna os registros recuperados
    return rows


# Função para excluir um registro com base no ID
def delete(id):
    conn = sqlite3.connect("banco_de_dados.db")
    cur = conn.cursor()
    # Executa o comando SQL para excluir o registro com o ID fornecido
    cur.execute("DELETE FROM banco_de_dados WHERE id=?", (id,))
    conn.commit()
    conn.close()


# Função que atualiza um registro com base no ID
def update(id, titulo, plataforma, estoque, valor, codigo):
    print("Atualizando:", id, titulo, plataforma, estoque, valor, codigo)
    conn = sqlite3.connect("banco_de_dados.db")
    cur = conn.cursor()
    # Executa o comando SQL para excluir o registro com o ID fornecido
    cur.execute("UPDATE banco_de_dados SET titulo=?, plataforma=?, estoque=?, valor=?, codigo=? WHERE id=?",
                (titulo, plataforma, estoque, valor, codigo, id))
    conn.commit()
    conn.close()
    print("Atualização concluída.")


# Função para verificar se um código já existe no banco de dados
def code_exists(codigo):
    conn = sqlite3.connect("banco_de_dados.db")
    cur = conn.cursor()
    # Executa o comando SQL para buscar um registro com o código fornecido
    cur.execute("SELECT * FROM banco_de_dados WHERE codigo=?", (codigo,))
    # Recupera o registro encontrado
    row = cur.fetchone()
    conn.close()

    # Retorna True se o código existe, False se não existe
    return row is not None


# Função para salvar os dados do banco de dados em um arquivo de texto temporário
def save_file():
    # Conecta ao banco de dados
    conn = sqlite3.connect("banco_de_dados.db")
    cur = conn.cursor()
    # Anexa um banco de dados temporário à memória e cria uma tabela temporária com os dados
    cur.execute("ATTACH DATABASE ':memory:' AS memdb")
    cur.execute("CREATE TABLE memdb.banco_de_dados AS SELECT * FROM banco_de_dados")

    # Abre o arquivo 'tarefas_temp.txt' em modo de escrita
    with open("tarefas_temp.txt", "w") as file:
        # Itera sobre cada linha da representação em texto do banco de dados
        for line in conn.iterdump():
            # Escreve a linha no arquivo
            file.write(f"{line}\n")
    conn.close()


# Função para carregar os dados do arquivo de texto temporário de volta para o banco de dados
def load_file():
    # Verifica se o arquivo 'tarefas_temp.txt' existe
    if os.path.exists("tarefas_temp.txt"):
        conn = sqlite3.connect("banco_de_dados.db")
        cur = conn.cursor()
        # Anexa o banco de dados temporário do arquivo
        cur.execute("ATTACH DATABASE 'tarefas_temp.txt' AS tempdb")
        # Seleciona todos os registros da tabela temporária no arquivo
        cur.execute("SELECT * FROM tempdb.banco_de_dados")
        # Recupera todos os registros
        rows = cur.fetchall()
        conn.close()
        # Retorna as linhas com os registros recuperados
        return rows
    else:
        # Se o arquivo não existe, retorna uma lista vazia
        return []


# Conecta ao banco de dados ao iniciar o script
connect()

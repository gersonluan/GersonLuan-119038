#FILME (filme_id, filme_nome)
#CLIENTE (nome_id, nome_cliente)
#PEDIDO (pedido_nome, pedido_filme)

from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import psycopg2 
  
app = Flask(__name__) 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
 
 
@app.route("/")
def index():
    if not session.get("username"):
        return redirect("/login")
    return render_template('index.html')
 
 
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session["username"] = request.form.get("username")
        return redirect("/filmesdb")
    return render_template("login.html")
 
 
@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/")

# Conecta ao banco de dados
conn = psycopg2.connect(database="flask_db", user="postgres", 
                        password="root", host="localhost", port="5959") 
  
#Cria um cursor
cur = conn.cursor() 
  
#Irá criar a tabela de filmes e clientes
cur.execute( 
    '''CREATE TABLE IF NOT EXISTS filme (filme_id serial \ 
    PRIMARY KEY, filme_nome varchar(100));''') 

cur.execute( 
    '''CREATE TABLE IF NOT EXISTS cliente (nome_id serial \ 
    PRIMARY KEY, nome_cliente(100));''') 

cur.execute( 
    '''CREATE TABLE IF NOT EXISTS pedido (pedido_nome serial, pedido_filme serial);''') 

#Alterar tabelas para adicionar uma chave estrangeira
cur.execute(
    '''ALTER TABLE pedido ADD FOREIGN KEY(pedido_nome) REFERENCES cliente(nome_id);''')

cur.execute(
    '''ALTER TABLE pedido ADD FOREIGN KEY(pedido_filme) REFERENCES filme(filme_id);''')

# Exemplos de dados adicionados
cur.execute( 
    '''INSERT INTO filme (filme_nome) VALUES \ 
    ('Star Wars'), ('Os Incriveis'), ('Kung Fu Panda');''') 
  
# Efetiva as alterações
conn.commit() 
  
# Fecha o cursor e a conexão
cur.close() 
conn.close() 
  
  
@app.route('/filmesdb') 
def index(): 
    # Conecta com o banco de dados
    conn = psycopg2.connect(database="flask_db", 
                            user="postgres", 
                            password="root", 
                            host="localhost", port="5959") 
  
    # Cria um cursor
    cur = conn.cursor() 
  
    # Seleciona todos os dados
    cur.execute('''SELECT * FROM filmes''') 
  
    # Busca pelos dados
    data = cur.fetchall() 
  
    # Fecha o cursor e a conexão
    cur.close() 
    conn.close() 
  
    return render_template('index.html', data=data) 
  
  
@app.route('/create', methods=['POST']) 
def create(): 
    conn = psycopg2.connect(database="flask_db", 
                            user="postgres", 
                            password="root", 
                            host="localhost", port="5959") 
  
    cur = conn.cursor() 
  
    # Pega o dado da tabela 
    filme_nome = request.form['filme_nome'] 
    
  
    # Insert the data into the table 
    cur.execute( 
        '''INSERT INTO filme \ 
        (filme_nome) VALUES (%s)''', 
        (filme_nome)) 
  
    # commit the changes 
    conn.commit() 
  
    # close the cursor and connection 
    cur.close() 
    conn.close() 
  
    return redirect(url_for('index')) 
  
  
@app.route('/update', methods=['POST']) 
def update(): 
    conn = psycopg2.connect(database="flask_db", 
                            user="postgres", 
                            password="root", 
                            host="localhost", port="5959") 
  
    cur = conn.cursor() 
  
    # Pega os dados da tabela
    filme_nome = request.form['filme_nome'] 
    filme_id = request.form['filme_id'] 
  
    # Atualiza os dados
    cur.execute( 
        '''UPDATE filme SET filme_nome=%s WHERE filme_id=%s''', (filme_nome, filme_id)) 
  
    # Efetiva as alterações
    conn.commit() 
    return redirect(url_for('index')) 
  
  
@app.route('/delete', methods=['POST']) 
def delete(): 
    conn = psycopg2.connect (database="flask_db", user="postgres", 
     password="root", 
     host="localhost", port="5959") 
    cur = conn.cursor() 
  
    # Pega os dados da tabela
    filme_id = request.form['filme_id'] 
  
    # Deleta os dados da tabela
    cur.execute('''DELETE FROM filme WHERE filme_id=%s''', (filme_id,)) 
  
    # Efetiva as alterações
    conn.commit() 
  
    # Fecha o cursor e a conexão
    cur.close() 
    conn.close() 
  
    return redirect(url_for('index')) 
  
if __name__ == '__main__': 
    app.run(debug=True) 
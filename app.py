from flask import Flask, request, jsonify, send_from_directory
import pyodbc

app = Flask(__name__)

# Conectar ao banco de dados SQL Server
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-G7JP4L7\SQLEXPRESS;DATABASE=projeto_web;UID='';PWD=''')
cursor = conn.cursor()

# Criar tabela de usuários se não existir
cursor.execute('''
    
''')
conn.commit()

# Rota para servir arquivos estáticos (HTML, CSS, JS, etc.)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    data = request.json
    nome = data['nome']
    email = data['email']
    password = data['password']
    cursor.execute('INSERT INTO usuarios (nome, email, password) VALUES (?, ?, ?)', (nome, email, password))
    conn.commit()
    return jsonify({'message': 'Usuário cadastrado com sucesso!'})

@app.route('/login', methods=['POST'])
def fazer_login():
    data = request.json
    email = data['email']
    password = data['password']
    cursor.execute('SELECT * FROM usuarios WHERE email = ? AND password = ?', (email, password))
    usuario = cursor.fetchone()
    if usuario:
        return jsonify({'message': 'Login bem-sucedido!'})
    else:
        return jsonify({'message': 'Credenciais inválidas!'}), 401

if __name__ == '__main__':
    app.run(debug=True)

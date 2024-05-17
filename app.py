from flask import Flask, request, jsonify, send_from_directory
import pyodbc
import bcrypt

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

    # Gerar hash da senha
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        cursor.execute('INSERT INTO usuarios (nome, email, password) VALUES (?, ?, ?)', (nome, email, password_hash))
        conn.commit()
        return jsonify({'message': 'Usuário cadastrado com sucesso!'})
    except Exception as e:
        return jsonify({'message': 'Erro ao cadastrar usuário: {}'.format(str(e))}), 500


@app.route('/login', methods=['POST'])
def fazer_login():
    email = request.form.get('email')
    senha = request.form.get('password')

    try:
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario = cursor.fetchone()

        if usuario:
            # Verificar a senha hasheada
            if bcrypt.checkpw(senha.encode('utf-8'), usuario.password.encode('utf-8')):
                return jsonify({'message': 'Login bem-sucedido!'})
            else:
                return jsonify({'message': 'Credenciais inválidas!'}), 401
        else:
            return jsonify({'message': 'Credenciais inválidas!'}), 401
    except Exception as e:
        return jsonify({'message': 'Erro ao fazer login: {}'.format(str(e))}), 500


if __name__ == '__main__':
    app.run(debug=True)

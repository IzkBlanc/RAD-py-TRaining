import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

conexao = sqlite3.connect('alunos.db')

conexao.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nota REAL NOT NULL
    )
''')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/alunos')
def alunos():
    cursor = conexao.execute('SELECT * FROM alunos')
    alunos = cursor.fetchall()
    return render_template('alunos.html', alunos=alunos)

@app.route('/cadastrar_aluno', methods=['POST'])
def cadastrar_aluno():
    nome = request.form['nome']
    nota = request.form['nota']
    cursor = conexao.execute('SELECT COUNT(*) FROM alunos WHERE nome = ?', (nome,))
    count = cursor.fetchone()[0]
    if count == 0:
        conexao.execute('INSERT INTO alunos (nome, nota) VALUES (?, ?)', (nome, nota))
        conexao.commit()
        return 'Aluno cadastrado com sucesso!'
    else:
        return 'Erro: Este aluno já está cadastrado.'

if __name__ == "__main__":
    app.run(debug=True)

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Configuração do Banco de Dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS alunos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, curso TEXT NOT NULL)')
    conn.commit()
    conn.close()

# --- ROTAS DO SITE (HTML) ---
@app.route('/')
def index():
    conn = get_db_connection()
    alunos = conn.execute('SELECT * FROM alunos').fetchall()
    conn.close
    return render_template('index.html', alunos=alunos)

@app.route('/add', methods=['POST'])
def add_aluno():
    nome = request.form['nome']
    curso = request.form['curso']
    if nome and curso:
        conn = get_db_connection()
        conn.execute('INSERT INTO alunos (nome, curso) VALUES (?, ?)', (nome, curso))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_aluno(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM alunos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# --- ROTA DE API (JSON) ---
@app.route('/api/alunos', methods=['GET'])
def get_alunos_json():
    conn = get_db_connection()
    alunos = conn.execute('SELECT * FROM alunos').fetchall()
    conn.close()

    # Transformar os objetos do banco de dados sqlite
    # em uma lista de dicionários
    lista_alunos = [dict(aluno) for aluno in alunos]
    return jsonify(lista_alunos)

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
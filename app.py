from flask import Flask, render_template, request, redirect, send_file, session
import sqlite3
from datetime import datetime
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
import os

# --- Configurações do app ---
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')

# --- Senha do admin ---
ADMIN_PASSWORD_HASH = generate_password_hash(os.environ.get('ADMIN_PASSWORD', 'icna@1997'))

# --- Banco de dados ---
def init_db():
    conn = sqlite3.connect('banco.db')
    c = conn.cursor()

    # Cria tabela se não existir com colunas básicas
    c.execute('''
    CREATE TABLE IF NOT EXISTS checkins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        tipo TEXT,
        data TEXT,
        dia TEXT,
        mes TEXT
    )
    ''')

    # Lista de colunas que queremos garantir na tabela
    colunas_necessarias = ['ministério', 'dia_semana']

    # Pega as colunas existentes
    c.execute("PRAGMA table_info(checkins)")
    colunas_existentes = [col[1] for col in c.fetchall()]

    # Adiciona colunas que não existem
    for col in colunas_necessarias:
        if col not in colunas_existentes:
            c.execute(f"ALTER TABLE checkins ADD COLUMN {col} TEXT")

    conn.commit()
    conn.close()

init_db()

# --- Rotas públicas ---
@app.route('/', methods=['GET', 'POST'])
def checkin():
    if request.method == 'POST':
        nome = request.form.get('nome', '')
        tipo = request.form.get('tipo', '')
        ministério = request.form.get('ministério', '')
        dia_semana = request.form.get('dia_semana', '')
        hoje = datetime.now()

        conn = sqlite3.connect('banco.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO checkins (nome, tipo, ministério, dia_semana, data, dia, mes) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (nome, tipo, ministério, dia_semana, hoje.strftime('%Y-%m-%d'), hoje.strftime('%d'), hoje.strftime('%m'))
        )
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('checkin.html')

# --- Login Admin ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form.get('senha', '')
        if check_password_hash(ADMIN_PASSWORD_HASH, senha):
            session['admin_logged_in'] = True
            return redirect('/admin')
        else:
            return render_template('login.html', erro="Senha incorreta")
    return render_template('login.html')

# --- Rotas Admin ---
@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        return redirect('/login')
    return render_template('admin.html')

@app.route('/admin/relatorios')
def relatorios():
    if not session.get('admin_logged_in'):
        return redirect('/login')
    return render_template('relatorios.html')

@app.route('/admin/exportar')
def exportar():
    if not session.get('admin_logged_in'):
        return redirect('/login')

    tipo = request.args.get('tipo', 'Voluntário')
    mes = request.args.get('mes', datetime.now().strftime('%m'))

    conn = sqlite3.connect('banco.db')
    query = "SELECT nome, tipo, ministério, dia_semana, dia, mes FROM checkins WHERE mes = ? AND tipo = ?"
    df = pd.read_sql_query(query, conn, params=(mes, tipo))
    conn.close()

    arquivo = f"{tipo.lower()}s_{mes}.xlsx"
    df.to_excel(arquivo, index=False)
    return send_file(arquivo, as_attachment=True)

# --- Logout ---
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect('/login')

# --- Context processor para footer ---
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# --- Main ---
if __name__ == '__main__':
    app.run(debug=True)

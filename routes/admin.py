import os
import sqlite3
import pandas as pd
from functools import wraps
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_file
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# carregar variáveis do .env
load_dotenv()

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# senha do admin (vem do .env)
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')
ADMIN_PASSWORD_HASH = generate_password_hash(ADMIN_PASSWORD)


# =========================
# DECORATOR DE PROTEÇÃO
# =========================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logado'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function


# =========================
# LOGIN
# =========================
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form.get('senha')

        if check_password_hash(ADMIN_PASSWORD_HASH, senha):
            session['admin_logado'] = True
            return redirect(url_for('admin.dashboard'))

        return render_template('login.html', erro='Senha inválida')

    return render_template('login.html')


# =========================
# LOGOUT
# =========================
@admin_bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('admin.login'))


# =========================
# DASHBOARD ADMIN
# =========================
@admin_bp.route('/')
@login_required
def dashboard():
    conn = sqlite3.connect('banco.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM checkins")
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM checkins WHERE tipo = 'Visitante'")
    visitantes = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM checkins WHERE tipo = 'Membro'")
    membros = c.fetchone()[0]

    conn.close()

    return render_template(
        'admin.html',
        total=total,
        visitantes=visitantes,
        membros=membros,
        grafico_labels=['Visitantes', 'Membros'],
        grafico_valores=[visitantes, membros]
    )




# =========================
# RELATÓRIOS
# =========================
@admin_bp.route('/relatorios')
@login_required
def relatorios():
    mes = request.args.get('mes')
    tipo = request.args.get('tipo')

    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = "SELECT nome, tipo, dia, mes FROM checkins WHERE 1=1"
    params = []

    if mes:
        query += " AND mes = ?"
        params.append(mes)

    if tipo:
        query += " AND tipo = ?"
        params.append(tipo)

    c.execute(query, params)
    registros = c.fetchall()
    conn.close()

    return render_template(
        'relatorios.html',
        registros=registros,
        mes=mes,
        tipo=tipo
    )


# =========================
# EXPORTAR EXCEL
# =========================
@admin_bp.route('/exportar')
@login_required
def exportar():
    mes = request.args.get('mes')
    tipo = request.args.get('tipo')

    conn = sqlite3.connect('banco.db')

    query = "SELECT nome, tipo, dia, mes FROM checkins WHERE 1=1"
    params = []

    if mes:
        query += " AND mes = ?"
        params.append(mes)

    if tipo:
        query += " AND tipo = ?"
        params.append(tipo)

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    arquivo = 'relatorio_checkins.xlsx'
    df.to_excel(arquivo, index=False)

    return send_file(arquivo, as_attachment=True)

from flask import Blueprint, render_template, request, session, redirect, send_file
import sqlite3
import pandas as pd

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_home():
    if not session.get('admin_logged_in'):
        return redirect('/login')
    return render_template('admin.html')

@admin_bp.route('/relatorios')
def relatorios():
    if not session.get('admin_logged_in'):
        return redirect('/login')
    tipo = request.args.get('tipo', 'Visitante')
    mes = request.args.get('mes', None)
    conn = sqlite3.connect('banco.db')
    query = "SELECT nome, tipo, ministério, dia, mes, dia_semana FROM checkins"
    if tipo:
        query += " WHERE tipo = ?"
        params = (tipo,)
    else:
        params = ()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return render_template('relatorios.html', tabelas=[df.to_html(classes='table', index=False)], tipo=tipo)

@admin_bp.route('/exportar')
def exportar():
    if not session.get('admin_logged_in'):
        return redirect('/login')
    tipo = request.args.get('tipo', 'Visitante')
    conn = sqlite3.connect('banco.db')
    query = "SELECT nome, tipo, ministério, dia, mes, dia_semana FROM checkins WHERE tipo = ?"
    df = pd.read_sql_query(query, conn, params=(tipo,))
    conn.close()
    arquivo = f"{tipo.lower()}s.xlsx"
    df.to_excel(arquivo, index=False)
    return send_file(arquivo, as_attachment=True)

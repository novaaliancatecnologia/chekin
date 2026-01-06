from flask import Blueprint, render_template, request, redirect
import sqlite3
from datetime import datetime

public_bp = Blueprint('public', __name__)

@public_bp.route('/', methods=['GET', 'POST'])
def checkin(ministério=None):
    if request.method == 'POST':
        nome = request.form['nome']
        tipo = request.form['tipo']
        ministério = request.form.get('ministério', '')  # só para Voluntário
        hoje = datetime.now()
        dia_semana = hoje.strftime('%A')
        dia = hoje.strftime('%d')
        mes = hoje.strftime('%m')

        conn = sqlite3.connect('banco.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO checkins (nome, tipo, ministério, dia, mes, dia_semana)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, tipo, ministério, dia, mes, dia_semana))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('checkin.html')

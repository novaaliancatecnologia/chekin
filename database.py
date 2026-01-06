import sqlite3
from datetime import datetime

DB_NAME = 'banco.db'

def conectar():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = conectar()
    c = conn.cursor()
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
    conn.commit()
    conn.close()

def inserir_checkin(nome, tipo):
    hoje = datetime.now()
    conn = conectar()
    c = conn.cursor()
    c.execute(
        "INSERT INTO checkins (nome, tipo, data, dia, mes) VALUES (?, ?, ?, ?, ?)",
        (nome, tipo, hoje.strftime('%Y-%m-%d'), hoje.strftime('%d'), hoje.strftime('%m'))
    )
    conn.commit()
    conn.close()

def listar_checkins():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM checkins ORDER BY id DESC")
    dados = c.fetchall()
    conn.close()
    return dados

def filtrar_checkins(mes=None, tipo=None):
    conn = conectar()
    c = conn.cursor()

    query = "SELECT * FROM checkins WHERE 1=1"
    params = []

    if mes:
        query += " AND mes = ?"
        params.append(mes)

    if tipo:
        query += " AND tipo = ?"
        params.append(tipo)

    query += " ORDER BY id DESC"

    c.execute(query, params)
    dados = c.fetchall()
    conn.close()
    return dados

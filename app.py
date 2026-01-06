from flask import Flask
from routes.public import public_bp
from routes.admin import admin_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.register_blueprint(public_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True)




# senha admin (hash)
ADMIN_PASSWORD_HASH = generate_password_hash('icna@1997')

# banco
init_db()

# registrar rotas
app.register_blueprint(public_bp)
app.register_blueprint(admin_bp)

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    from flask import request, render_template

    erro = None
    if request.method == 'POST':
        if check_password_hash(ADMIN_PASSWORD_HASH, request.form['senha']):
            session['admin'] = True
            return redirect('/admin')
        else:
            erro = 'Senha inválida'

    return render_template('login.html', erro=erro)

# logout
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


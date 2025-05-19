from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = '1234567890'

def get_db_connection():
    conn = sqlite3.connect('comercio.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        senha = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE nome = ? AND senha = ?', (usuario, senha)).fetchone()
        conn.close()

        if user:
            session['username'] = user['nome']  # Salva na sessão
            return redirect(url_for('user'))    # Redireciona para página do usuário logado
        else:
            flash('Login inválido. Tente novamente.')
            return redirect(url_for('login'))

    return render_template('login.html')  # Mostrar form de login

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
            conn.commit()
            flash('Cadastro realizado com sucesso!')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email já cadastrado!')
            return redirect(url_for('register'))
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()  # Limpa sessão
    flash('Você saiu com sucesso!')
    return redirect(url_for('login'))

@app.route('/user')
def user():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('user.html', username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)

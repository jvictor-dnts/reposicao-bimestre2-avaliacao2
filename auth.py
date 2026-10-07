from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import database

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not nome or not email or not senha:
            flash('Preencha todos os campos!')
            return redirect(url_for('auth.registro'))

        if database.buscar_usuario_por_email(email):
            flash('E-mail já cadastrado!')
            return redirect(url_for('auth.registro'))

        senha_hash = generate_password_hash(senha)
        database.criar_usuario(nome, email, senha_hash)

        return redirect(url_for('auth.login'))

    return render_template('registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = database.buscar_usuario_por_email(email)

        if usuario and check_password_hash(usuario['senha'], senha):
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            return redirect(url_for('index'))
        else:
            flash('E-mail ou senha incorretos.')
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/treinos')
def treinos():
    if 'usuario_id' not in session:
        return redirect(url_for('auth.login'))
    return redirect(url_for('index'))

@auth_bp.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_nome', None)
    return redirect(url_for('auth.login'))
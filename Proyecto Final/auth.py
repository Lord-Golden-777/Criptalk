# auth.py
# Blueprint para autenticación: registro, login y logout

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User
from ext import db

# Crear blueprint para auth
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registro de usuario.
    GET: muestra formulario.
    POST: valida y crea usuario.
    """
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        # Validar si el username ya existe
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        # Validar si el email ya está registrado
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('auth.register'))

        # Crear nuevo usuario y guardarlo
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Login automático después del registro
        login_user(new_user)
        return redirect(url_for('chat.open_chat'))

    # Mostrar formulario de registro
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login de usuario.
    GET: muestra formulario.
    POST: valida credenciales y loguea.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Buscar usuario por username
        user = User.query.filter_by(username=username).first()

        # Validar contraseña
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('chat.open_chat'))

        # Mensaje de error si credenciales no válidas
        flash('Invalid credentials')

    # Mostrar formulario de login
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Cierra sesión del usuario.
    """
    logout_user()
    return redirect(url_for('auth.login'))

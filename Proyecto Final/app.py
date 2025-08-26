# app.py
# Archivo principal de la aplicación Flask

import os
from flask import Flask, redirect, url_for
from ext import db, login_manager, socketio  # extensiones inicializadas


def create_app():
    """Crea y configura la app Flask."""
    app = Flask(__name__)

    # Configuración básica
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "devkey")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Carpeta para uploads
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static",
                                               "uploads")
    # Tamaño máximo de archivos: 5 GB
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 ** 3

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    # Importar modelo User para login
    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        """Función para cargar usuario desde ID."""
        return User.query.get(int(user_id))

    # Ruta de login si no está autenticado
    login_manager.login_view = "auth.login"

    @app.route("/")
    def index():
        """Redirige a la página de login."""
        return redirect(url_for("auth.login"))

    # Importar blueprints
    from contacts import contacts_bp
    from chat import chat_bp
    from auth import auth_bp

    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(contacts_bp)

    return app


if __name__ == "__main__":
    # Ejecutar app
    app = create_app()
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
    socketio.run(app, debug=True)

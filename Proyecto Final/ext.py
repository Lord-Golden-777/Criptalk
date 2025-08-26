# ext.py
# Importación de extensiones de Flask necesarias para el proyecto
from flask_sqlalchemy import SQLAlchemy  # Para manejar la base de datos
from flask_login import LoginManager     # Para manejar la autenticación de
# usuarios
from flask_socketio import SocketIO      # Para comunicación en tiempo real

# Instancia de SQLAlchemy para manejar la base de datos
db = SQLAlchemy()

# Instancia de LoginManager para manejar login y sesiones de usuario
login_manager = LoginManager()

# Instancia de SocketIO para manejo de eventos en tiempo real
socketio = SocketIO()

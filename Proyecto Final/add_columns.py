# add_columns.py
# Script para añadir columnas "image_filename" a las tablas de mensajes

from app import create_app
from ext import db
from sqlalchemy import text

# Crear la app y activar el contexto
app = create_app()

with app.app_context():
    # Conectar a la base de datos
    conn = db.engine.connect()
    try:
        # Intentamos añadir columna "image_filename" a tabla message
        try:
            conn.execute(
                text(
                    "ALTER TABLE message "
                    "ADD COLUMN image_filename VARCHAR(300)"
                )
            )
            print("Columna image_filename añadida a message")
        except Exception as e:
            # Si ya existe o hay otro error
            print("No se añadió a message (quizá ya existe):", e)

        # Intentamos añadir columna "image_filename" a tabla group_messages
        try:
            conn.execute(
                text(
                    "ALTER TABLE group_messages "
                    "ADD COLUMN image_filename VARCHAR(300)"
                )
            )
            print("Columna image_filename añadida a group_messages")
        except Exception as e:
            # Si ya existe o hay otro error
            print("No se añadió a group_messages (quizá ya existe):", e)

    finally:
        # Cerrar la conexión
        conn.close()

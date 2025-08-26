# contacts.py
# Importación de módulos necesarios de Flask y Flask-Login
from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ext import db  # Importación de la extensión de base de datos
from models import User, Contact  # Importación de los modelos User y Contact

# Creación del blueprint para contactos
contacts_bp = Blueprint("contacts", __name__, url_prefix="/contacts")


# Función para verificar si dos usuarios ya son contactos
def are_already_contacts(a_id: int, b_id: int) -> bool:
    # Retorna True si existe un registro de contacto entre los dos IDs
    return (
        Contact.query.filter_by(user_id=a_id, contact_id=b_id).first() is not
        None
    )


# Ruta para agregar un contacto
@contacts_bp.route("/add", methods=["POST"])
@login_required  # Solo usuarios autenticados pueden acceder
def add_contact():
    # Obtiene el código del formulario y lo convierte a mayúsculas
    code = request.form.get("code", "").strip().upper()

    # Si no se proporciona un código válido, muestra mensaje de error
    if not code:
        flash("Ingresa un código válido.", "error")
        return redirect(url_for("chat.chat_room"))

    # Busca al usuario con el código proporcionado
    target = User.query.filter_by(code=code).first()
    if not target:
        flash("No existe un usuario con ese código.", "error")
        return redirect(url_for("chat.chat_room"))

    # Evita que un usuario se agregue a sí mismo
    if target.id == current_user.id:
        flash("No puedes agregarte a ti mismo.", "error")
        return redirect(url_for("chat.chat_room"))

    # Verifica si ya son contactos
    if are_already_contacts(current_user.id, target.id):
        flash("Ese usuario ya está en tus contactos.", "info")
        return redirect(url_for("chat.open_chat", contact_id=target.id))

    # Guardar relación en ambos sentidos (mutuo)
    db.session.add(Contact(user_id=current_user.id, contact_id=target.id))
    db.session.add(Contact(user_id=target.id, contact_id=current_user.id))
    db.session.commit()

    # Mensaje de éxito y redirección al chat con el nuevo contacto
    flash("Contacto agregado correctamente.", "success")
    return redirect(url_for("chat.open_chat", contact_id=target.id))

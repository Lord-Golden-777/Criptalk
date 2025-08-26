# models.py
# Importaciones necesarias
import random
import string
from datetime import datetime

from flask_login import UserMixin  # Para el manejo de sesiones de usuario

from app import db  # Importación de la instancia de SQLAlchemy


# Función para generar un código aleatorio de usuario
def generate_code(length=5):
    """Genera un código aleatorio de `length` caracteres."""
    return "".join(
        random.choices(string.ascii_uppercase + string.digits, k=length)
    )


# Modelo de usuario
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    code = db.Column(
        db.String(5),
        unique=True,
        nullable=False,
        default=generate_code,
    )

    # Relación con contactos (uno a muchos)
    contacts = db.relationship(
        "Contact",
        foreign_keys="Contact.user_id",
        backref="user",
        lazy=True,
    )


# Modelo de contacto
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )
    contact_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )

    # Relación con el usuario que es el contacto
    contact_user = db.relationship("User", foreign_keys=[contact_id])


# Modelo de mensaje privado
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)  # puede ser solo imagen
    image_filename = db.Column(db.String(300), nullable=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"),
                            nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# Modelo de grupo
class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con miembros y mensajes del grupo
    members = db.relationship(
        "GroupMember",
        back_populates="group",
        cascade="all, delete-orphan",
    )
    messages = db.relationship(
        "GroupMessage",
        back_populates="group",
        cascade="all, delete-orphan",
    )


# Modelo de miembro de grupo
class GroupMember(db.Model):
    __tablename__ = "group_members"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"),
                         nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con el grupo y el usuario
    group = db.relationship("Group", back_populates="members")
    user = db.relationship("User", backref="group_memberships")


# Modelo de mensaje de grupo
class GroupMessage(db.Model):
    __tablename__ = "group_messages"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"),
                         nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(300), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación con el grupo y el remitente
    group = db.relationship("Group", back_populates="messages")
    sender = db.relationship("User", backref="group_messages")

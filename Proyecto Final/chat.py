# chat.py
import os
import uuid
import difflib
from datetime import datetime
from werkzeug.utils import secure_filename

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
)
from flask_login import current_user, login_required
from flask_socketio import emit, join_room
from sqlalchemy import or_

# importar desde ext para evitar ciclos con app.py
from ext import db, socketio

from models import (
    User,
    Message,
    Contact,
    Group,
    GroupMember,
    GroupMessage,
)

chat_bp = Blueprint("chat", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def _allowed_file(filename):
    if not filename:
        return False
    ext = filename.rsplit(".", 1)[-1].lower()
    return ext in ALLOWED_EXTENSIONS


def _save_uploaded_file(file_storage):
    upload_folder = current_app.config.get("UPLOAD_FOLDER")
    if not upload_folder:
        upload_folder = os.path.join(current_app.root_path, "static",
        "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(file_storage.filename)
    if not _allowed_file(filename):
        return None

    unique_name = f"{uuid.uuid4().hex}_{filename}"
    path = os.path.join(upload_folder, unique_name)
    file_storage.save(path)
    return unique_name


def _get_contacts_for_user(user):
    if not user:
        return []

    contacts = []
    try:
        if Contact is not None:
            rows = Contact.query.filter_by(user_id=user.id).all()
            for r in rows:
                other = User.query.get(getattr(r, "contact_id", None))
                if other:
                    contacts.append(other)
        else:
            if hasattr(user, "contacts"):
                contacts = list(user.contacts) if user.contacts else []
    except Exception as exc:
        current_app.logger.exception(exc)
        contacts = []

    return contacts


def _get_groups_for_user(user):
    if not user:
        return []

    groups = []
    try:
        rows = GroupMember.query.filter_by(user_id=user.id).all()
        for r in rows:
            g = Group.query.get(getattr(r, "group_id", None))
            if g:
                groups.append(g)
    except Exception as exc:
        current_app.logger.exception(exc)
        groups = []

    return groups


@chat_bp.route("/chat/", defaults={"contact_id": None}, methods=["GET"])
@chat_bp.route("/chat/<int:contact_id>", methods=["GET"])
@login_required
def open_chat(contact_id):
    active_contact = None
    messages = []

    if contact_id is not None:
        active_contact = User.query.get(contact_id)
        if not active_contact:
            flash("Contacto no encontrado.", "warning")
            return redirect(url_for("chat.open_chat"))

        try:
            messages = (
                Message.query.filter(
                    ((Message.sender_id == current_user.id)
                     & (Message.receiver_id == active_contact.id))
                    | ((Message.sender_id == active_contact.id)
                       & (Message.receiver_id == current_user.id))
                )
                .order_by(Message.timestamp.asc())
                .all()
            )
        except Exception as exc:
            current_app.logger.exception(exc)
            messages = []

    contacts = _get_contacts_for_user(current_user)
    groups = _get_groups_for_user(current_user)
    highlight_id = request.args.get("highlight_id")

    return render_template(
        "chat.html",
        active_contact=active_contact,
        messages=messages,
        contacts=contacts,
        groups=groups,
        user_id=current_user.id,
        username=current_user.username,
        user_code=getattr(current_user, "code", ""),
        highlight_message_id=highlight_id,
    )


@chat_bp.route("/group/<int:group_id>", methods=["GET"])
@login_required
def open_group(group_id):
    group = Group.query.get(group_id)
    if not group:
        flash("Grupo no encontrado.", "warning")
        return redirect(url_for("chat.open_chat"))

    membership = GroupMember.query.filter_by(
        group_id=group_id, user_id=current_user.id
    ).first()
    if not membership:
        flash("No eres miembro de este grupo.", "warning")
        return redirect(url_for("chat.open_chat"))

    try:
        messages = (
            GroupMessage.query.filter_by(group_id=group_id)
            .order_by(GroupMessage.timestamp.asc())
            .all()
        )
    except Exception as exc:
        current_app.logger.exception(exc)
        messages = []

    contacts = _get_contacts_for_user(current_user)
    groups = _get_groups_for_user(current_user)
    highlight_id = request.args.get("highlight_id")

    return render_template(
        "chat.html",
        active_group=group,
        messages=messages,
        contacts=contacts,
        groups=groups,
        user_id=current_user.id,
        username=current_user.username,
        user_code=getattr(current_user, "code", ""),
        highlight_message_id=highlight_id,
    )


@chat_bp.route("/group/create", methods=["GET", "POST"])
@login_required
def create_group():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        codes = (request.form.get("codes") or "").strip()

        if not name:
            flash("Debe ingresar un nombre para el grupo.", "warning")
            return redirect(url_for("chat.create_group"))

        group = Group(name=name, owner_id=current_user.id)
        db.session.add(group)
        db.session.flush()

        gm_self = GroupMember(group_id=group.id, user_id=current_user.id)
        db.session.add(gm_self)

        if codes:
            for code in (c.strip() for c in codes.split(",") if c.strip()):
                user_to_add = User.query.filter_by(code=code).first()
                if user_to_add and user_to_add.id != current_user.id:
                    exists = GroupMember.query.filter_by(
                        group_id=group.id, user_id=user_to_add.id
                    ).first()
                    if not exists:
                        db.session.add(
                            GroupMember(group_id=group.id,
                                        user_id=user_to_add.id)
                        )

        db.session.commit()
        flash("Grupo creado.", "success")
        return redirect(url_for("chat.open_group", group_id=group.id))

    return render_template("create_group.html")


@chat_bp.route("/contact/remove/<int:contact_id>", methods=["POST"])
@login_required
def remove_contact(contact_id):
    try:
        row = Contact.query.filter_by(
            user_id=current_user.id, contact_id=contact_id
        ).first()
        if not row:
            flash("Contacto no encontrado o ya eliminado.", "warning")
            return redirect(url_for("chat.open_chat"))

        db.session.delete(row)
        db.session.commit()
        flash("Contacto eliminado.", "success")
    except Exception as exc:
        db.session.rollback()
        current_app.logger.exception(exc)
        flash("No se pudo eliminar el contacto.", "danger")

    return redirect(url_for("chat.open_chat"))


@chat_bp.route("/group/<int:group_id>/leave", methods=["POST"])
@login_required
def leave_group(group_id):
    try:
        group = Group.query.get(group_id)
        if not group:
            flash("Grupo no encontrado.", "warning")
            return redirect(url_for("chat.open_chat"))

        if group.owner_id == current_user.id:
            flash(
                "Eres el creador del grupo. Si quieres eliminarlo, usa la "
                "opción Eliminar.",
                "warning",
            )
            return redirect(url_for("chat.open_group", group_id=group_id))

        membership = GroupMember.query.filter_by(
            group_id=group_id, user_id=current_user.id
        ).first()
        if not membership:
            flash("No eres miembro de este grupo.", "warning")
            return redirect(url_for("chat.open_chat"))

        db.session.delete(membership)
        db.session.commit()
        flash("Has salido del grupo.", "success")
    except Exception as exc:
        db.session.rollback()
        current_app.logger.exception(exc)
        flash("No se pudo salir del grupo.", "danger")

    return redirect(url_for("chat.open_chat"))


@chat_bp.route("/group/<int:group_id>/delete", methods=["POST"])
@login_required
def delete_group(group_id):
    try:
        group = Group.query.get(group_id)
        if not group:
            flash("Grupo no encontrado.", "warning")
            return redirect(url_for("chat.open_chat"))

        if group.owner_id != current_user.id:
            flash("Solo el creador puede eliminar el grupo.", "warning")
            return redirect(url_for("chat.open_group", group_id=group_id))

        db.session.delete(group)
        db.session.commit()
        flash("Grupo eliminado.", "success")
    except Exception as exc:
        db.session.rollback()
        current_app.logger.exception(exc)
        flash("No se pudo eliminar el grupo.", "danger")

    return redirect(url_for("chat.open_chat"))


@socketio.on("connect")
def handle_connect():
    try:
        if current_user.is_authenticated:
            join_room(f"user_{current_user.id}")
    except Exception as exc:
        current_app.logger.debug("connect: %s", exc)


@socketio.on("send_message")
def handle_send_message(data):
    try:
        content = data.get("content")
        contact_id = data.get("contact_id")
        if not content or contact_id is None:
            return

        msg = Message(
            sender_id=current_user.id,
            receiver_id=int(contact_id),
            content=content,
            timestamp=datetime.utcnow(),
        )
        db.session.add(msg)
        db.session.commit()

        payload = {
            "id": msg.id,
            "content": msg.content,
            "image_url": None,
            "time": msg.timestamp.strftime("%H:%M"),
            "sender_id": current_user.id,
        }

        emit("receive_message", payload, room=f"user_{current_user.id}")
        emit("receive_message", payload, room=f"user_{contact_id}")
    except Exception as exc:
        current_app.logger.exception(exc)


@socketio.on("join_group")
def handle_join_group(data):
    try:
        group_id = data.get("group_id")
        if group_id is None:
            return

        gm = GroupMember.query.filter_by(
            group_id=group_id, user_id=current_user.id
        ).first()
        if gm:
            join_room(f"group_{group_id}")
    except Exception as exc:
        current_app.logger.exception(exc)


@socketio.on("send_group_message")
def handle_send_group_message(data):
    try:
        content = data.get("content")
        group_id = data.get("group_id")
        if not content or group_id is None:
            return

        gm = GroupMember.query.filter_by(
            group_id=group_id, user_id=current_user.id
        ).first()
        if not gm:
            return

        gmsg = GroupMessage(
            group_id=group_id,
            sender_id=current_user.id,
            content=content,
            timestamp=datetime.utcnow(),
        )
        db.session.add(gmsg)
        db.session.commit()

        payload = {
            "id": gmsg.id,
            "content": gmsg.content,
            "image_url": None,
            "time": gmsg.timestamp.strftime("%H:%M"),
            "sender_id": current_user.id,
            "group_id": group_id,
        }
        emit("receive_group_message", payload, room=f"group_{group_id}")
    except Exception as exc:
        current_app.logger.exception(exc)


# --- Upload endpoints (images) ---
@chat_bp.route("/upload_image", methods=["POST"])
@login_required
def upload_image():
    file = request.files.get("file")
    contact_id = request.form.get("contact_id") or request.form.get(
        "contactId")
    content = (request.form.get("content") or "").strip()

    if not file or not contact_id:
        return jsonify({"error": "Falta archivo o contact_id."}), 400

    filename = _save_uploaded_file(file)
    if not filename:
        return jsonify({"error": "Tipo de archivo no permitido."}), 400

    try:
        msg_content = content if content else ""
        msg = Message(
            content=msg_content,
            image_filename=filename,
            sender_id=current_user.id,
            receiver_id=int(contact_id),
            timestamp=datetime.utcnow(),
        )

        db.session.add(msg)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        current_app.logger.exception(exc)
        return jsonify({"error": "No se pudo guardar el mensaje."}), 500

    image_url = url_for("static", filename=f"uploads/{filename}",
                        _external=False)

    payload = {
        "id": msg.id,
        "content": msg.content,
        "image_url": image_url,
        "time": msg.timestamp.strftime("%H:%M"),
        "sender_id": current_user.id,
    }

    socketio.emit("receive_message", payload, room=f"user_{current_user.id}")
    socketio.emit("receive_message", payload, room=f"user_{contact_id}")

    return jsonify({"ok": True, "payload": payload})


@chat_bp.route("/upload_group_image", methods=["POST"])
@login_required
def upload_group_image():
    file = request.files.get("file")
    group_id = request.form.get("group_id") or request.form.get("groupId")
    content = (request.form.get("content") or "").strip()

    if not file or not group_id:
        return jsonify({"error": "Falta archivo o group_id."}), 400

    filename = _save_uploaded_file(file)
    if not filename:
        return jsonify({"error": "Tipo de archivo no permitido."}), 400

    gm = GroupMember.query.filter_by(group_id=group_id, user_id=current_user.
                                     id).first()
    if not gm:
        return jsonify({"error": "No miembro del grupo."}), 403

    try:
        gmsg_content = content if content else ""
        gmsg = GroupMessage(
            group_id=int(group_id),
            sender_id=current_user.id,
            content=gmsg_content,
            image_filename=filename,
            timestamp=datetime.utcnow(),
        )

        db.session.add(gmsg)
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        current_app.logger.exception(exc)
        return jsonify({"error": "No se pudo guardar el mensaje de grupo."
                        }), 500

    image_url = url_for("static", filename=f"uploads/{filename}",
                        _external=False)

    payload = {
        "id": gmsg.id,
        "content": gmsg.content,
        "image_url": image_url,
        "time": gmsg.timestamp.strftime("%H:%M"),
        "sender_id": current_user.id,
        "group_id": int(group_id),
    }

    socketio.emit("receive_group_message", payload, room=f"group_{group_id}")

    return jsonify({"ok": True, "payload": payload})


@chat_bp.route("/contacts/search", methods=["GET"])
@login_required
def contacts_search():
    """
    Busca entre los contactos del usuario por término 'q'.
    Devuelve JSON con matches.
    """
    q = (request.args.get("q") or "").strip()
    if not q:
        return jsonify(results=[])

    matches = []
    try:
        rows = Contact.query.filter_by(user_id=current_user.id).all()
        for r in rows:
            u = User.query.get(getattr(r, "contact_id", None))
            if not u:
                continue
            if (
                q.lower() in (u.username or "").lower()
                or q.lower() in (u.code or "").lower()
            ):

                matches.append({"id": u.id, "username": u.username,
                                "code": u.code})
    except Exception:
        try:
            for u in getattr(current_user, "contacts", []):
                if not u:
                    continue
                if (
                    q.lower() in (u.username or "").lower()
                    or q.lower() in (u.code or "").lower()
                ):
                    matches.append(
                {
                    "id": u.id,
                    "username": u.username,
                    "code": u.code,
                }
            )

        except Exception:
            matches = []

    return jsonify(results=matches)


@chat_bp.route("/search_messages", methods=["GET"])
@login_required
def search_messages():
    """
    Búsqueda difusa de mensajes.
    Params:
      - q: texto búsqueda
      - contact_id (opcional)
      - group_id (opcional)
    Devuelve JSON con matches ordenados por relevancia.
    """
    q = (request.args.get("q") or "").strip()
    if not q:
        return jsonify(results=[])

    contact_id = request.args.get("contact_id")
    group_id = request.args.get("group_id")

    # número de mensajes candidatos a evaluar (limite para rendimiento)
    CANDIDATE_LIMIT = 500

    def score_text(query, text):
        """Calcula un score combinado: substring boost + similarity ratio."""
        if not text:
            return 0.0
        text_l = text.lower()
        q_l = query.lower()

        score = 0.0
        if q_l in text_l:
            score += 1.5
        if text_l.startswith(q_l):
            score += 0.7
        try:
            ratio = difflib.SequenceMatcher(None, q_l, text_l).ratio()
            score += ratio
        except Exception:
            score += 0.0
        return score

    def make_result(m, extra=None):
        sender = User.query.get(m.sender_id)
        res = {
            "id": m.id,
            "content": m.content or "",
            "time": m.timestamp.strftime("%Y-%m-%d %H:%M"),
            "sender_id": m.sender_id,
            "sender_username": sender.username if sender else "?",
        }
        if extra:
            res.update(extra)
        return res

    results = []

    # Grupo
    if group_id:
        try:
            gid = int(group_id)
        except (TypeError, ValueError):
            return jsonify(results=[])
        msgs = (
            GroupMessage.query.filter_by(group_id=gid)
            .order_by(GroupMessage.timestamp.desc())
            .limit(CANDIDATE_LIMIT)
            .all()
        )
        scored = []
        for m in msgs:
            s = score_text(q, m.content or "")
            if s > 0.0:
                scored.append((s, m))
        scored.sort(key=lambda x: x[0], reverse=True)
        for s, m in scored[:50]:
            results.append(make_result(m, {"group_id": gid}))
        return jsonify(results=results)

    # Mensajes privados con contact_id
    if contact_id:
        try:
            cid = int(contact_id)
        except (TypeError, ValueError):
            return jsonify(results=[])
        msgs = (
            Message.query.filter(
                (
                    (Message.sender_id == current_user.id)
                    & (Message.receiver_id == cid)
                )
                | (
                    (Message.sender_id == cid)
                    & (Message.receiver_id == current_user.id)
                )
            )
            .order_by(Message.timestamp.desc())
            .limit(CANDIDATE_LIMIT)
            .all()
        )
        scored = []
        for m in msgs:
            s = score_text(q, m.content or "")
            if s > 0.0:
                scored.append((s, m))
        scored.sort(key=lambda x: x[0], reverse=True)
        for s, m in scored[:50]:
            results.append(make_result(m, {"contact_id": cid}))
        return jsonify(results=results)

    # Fallback: mensajes donde participa current_user
    msgs = (
        Message.query.filter(
            or_(Message.sender_id == current_user.id, Message.receiver_id ==
            current_user.id)
        )
        .order_by(Message.timestamp.desc())
        .limit(CANDIDATE_LIMIT)
        .all()
    )
    scored = []
    for m in msgs:
        s = score_text(q, m.content or "")
        if s > 0.0:
            other_id = m.receiver_id if m.sender_id == current_user.id else m.sender_id
            scored.append((s, m, other_id))
    scored.sort(key=lambda x: x[0], reverse=True)
    for s, m, other_id in scored[:50]:
        results.append(make_result(m, {"contact_id": other_id}))

    return jsonify(results=results)

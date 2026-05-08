# 💬 Criptalk

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com/Lord-Golden-777/Criptalk)

**Una aplicación de chat moderna, rápida y segura construida con Flask y WebSockets en tiempo real.**

[Características](#-características) • [Instalación](#-instalación) • [Uso](#-uso) • [Tecnologías](#-tecnologías)

</div>

---

## 📋 Sobre el proyecto

**Criptalk** es una plataforma de mensajería instantánea que permite a los usuarios comunicarse de forma segura y en tiempo real. Ya sea chats privados uno a uno o conversaciones grupales, Criptalk ofrece una experiencia fluida y moderna con soporte para envío de imágenes, búsqueda de mensajes y un sistema de contactos intuitivo.

Perfecta para proyectos personales, educativos o como base para aplicaciones de comunicación más complejas.

---

## ✨ Características

- 💬 **Chat privado en tiempo real** - Comunícate directamente con otros usuarios
- 👥 **Grupos de chat** - Crea y gestiona grupos de conversación
- 🖼️ **Envío de imágenes** - Comparte imágenes (PNG, JPG, GIF, WebP)
- 🔍 **Búsqueda inteligente** - Encuentra mensajes rápidamente en cualquier conversación
- 🆔 **Códigos únicos** - Sistema seguro para agregar contactos (código de 5 caracteres)
- 📱 **Interfaz responsive** - Funciona perfectamente en escritorio y dispositivos móviles
- 🔐 **Autenticación segura** - Login con contraseña hasheada
- ⚡ **WebSockets** - Comunicación instantánea sin retrasos

---

## 🛠️ Tecnologías

| Tecnología | Descripción |
|-----------|------------|
| **Python 3.8+** | Lenguaje base |
| **Flask** | Framework web ligero |
| **Flask-SocketIO** | WebSockets para tiempo real |
| **SQLAlchemy** | ORM para base de datos |
| **SQLite/PostgreSQL** | Base de datos |
| **HTML5/CSS3** | Frontend responsivo |
| **JavaScript vanilla** | Interactividad |

---

## 📦 Instalación

### Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos

**1. Clona el repositorio**
```bash
git clone https://github.com/Lord-Golden-777/Criptalk.git
cd Criptalk/Proyecto\ Final
```

**2. Crea un entorno virtual**
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Instala las dependencias**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**4. Ejecuta la aplicación**
```bash
python app.py
```

**5. Abre en tu navegador**
```
http://localhost:5000
```

---

## 🚀 Uso rápido

### Primer inicio

1. **Regístrate** con tu nombre de usuario y correo
2. **Comparte tu código** (5 caracteres) con otros usuarios
3. **Agrega contactos** usando sus códigos
4. **Comienza a chatear** en tiempo real
5. **Crea grupos** para conversaciones grupales

### Ejemplo de flujo

```
Usuario A                          Usuario B
   ↓                                  ↓
Comparte código: "ABC12"         Comparte código: "XYZ98"
   ↓                                  ↓
Agrega código "XYZ98"        ← → Agrega código "ABC12"
   ↓                                  ↓
¡Chat iniciado! 💬
```

---

## 📁 Estructura del proyecto

```
Proyecto Final/
├── app.py                  # 🚀 Punto de entrada
├── ext.py                  # ⚙️  Extensiones (DB, Login, SocketIO)
├── models.py               # 🗄️  Modelos de datos
├── auth.py                 # 🔐 Autenticación
├── chat.py                 # 💬 Rutas y WebSockets
├── contacts.py             # 👥 Gestión de contactos
│
├── templates/              # 📄 Plantillas HTML
│   ├── base.html          # Base para todas las páginas
│   ├── login.html         # Formulario de login
│   ├── register.html      # Formulario de registro
│   ├── chat.html          # Página principal del chat
│   └── contacts.html      # Gestión de contactos
│
├── static/                 # 🎨 Archivos estáticos
│   ├── style.css          # Estilos principales
│   ├── login.css          # Estilos del login
│   └── uploads/           # Imágenes subidas
│
└── requirements.txt        # 📦 Dependencias
```

---

## 🔒 Seguridad

- ✅ **Autenticación por sesión** - Usa Flask-Login
- ✅ **Contraseñas hasheadas** - Almacenamiento seguro con Werkzeug
- ✅ **Validación de archivos** - Solo extensiones permitidas (PNG, JPG, GIF, WebP)
- ✅ **Códigos únicos** - Cada usuario tiene un identificador seguro
- ✅ **CSRF Protection** - Integrado con Flask-WTF

> ⚠️ **Para producción:** Asegúrate de usar una `SECRET_KEY` fuerte y configurar correctamente las variables de entorno.

---

## 🎯 Casos de uso

- 🎓 **Educación** - Proyectos de clase de programación
- 👨‍💼 **Equipos pequeños** - Comunicación interna
- 🧪 **Prototipado** - Base para aplicaciones más grandes
- 🎮 **Comunidades** - Chat para grupos o comunidades

---

## 📝 Configuración (opcional)

Crea un archivo `.env` en la carpeta `Proyecto Final/`:

```bash
# .env
SECRET_KEY=tu_clave_super_segura_aqui
FLASK_ENV=development
DATABASE_URL=sqlite:///chat.db
```

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si quieres mejorar Criptalk:

1. **Fork** el repositorio
2. **Crea una rama** (`git checkout -b feature/mejora`)
3. **Haz commit** de tus cambios (`git commit -m 'Agrega mejora'`)
4. **Push** a la rama (`git push origin feature/mejora`)
5. **Abre un Pull Request**

### Áreas de mejora sugeridas
- [ ] Validación más robusta de contraseñas
- [ ] Cifrado de mensajes end-to-end
- [ ] Notificaciones push
- [ ] Temas oscuros/claros
- [ ] API REST
- [ ] Soporte para archivos más allá de imágenes

---

## 🐛 Reporte de problemas

¿Encontraste un bug? 🐛 [Abre un issue](https://github.com/Lord-Golden-777/Criptalk/issues) con:

- Descripción clara del problema
- Pasos para reproducirlo
- Versión de Python y navegador
- Screenshots (si aplica)

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Ver archivo [LICENSE](LICENSE) para más detalles.

---

## 🌟 ¿Te gustó el proyecto?

Si Criptalk te fue útil, considera darle una ⭐ en GitHub. ¡Significa mucho!

---

## 📞 Contacto

- **GitHub:** [@Lord-Golden-777](https://github.com/Lord-Golden-777)
- **Email:** Tu email aquí

---

<div align="center">

**Hecho con ❤️ por Adrian**

*Última actualización: 2026*

</div>

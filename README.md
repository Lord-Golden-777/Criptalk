# CripTalk

CripTalk es una aplicación web de mensajería en tiempo real construida con Flask. El proyecto está orientado a la comunicación rápida entre usuarios, con autenticación, persistencia de datos y una arquitectura modular pensada para crecer sin volverse caótica.

## Descripción

El objetivo de CripTalk es ofrecer una base sólida para un sistema de chat moderno donde el backend gestione:

- registro e inicio de sesión de usuarios,
- envío y recepción de mensajes en tiempo real,
- persistencia de información con base de datos,
- separación clara entre rutas, lógica de negocio y modelos,
- una interfaz web sencilla, responsive y fácil de mantener.

Este proyecto está pensado como práctica de desarrollo backend y full stack con Python, Flask, JavaScript y tecnologías web estándar.

## Cómo funciona

La aplicación se organiza en módulos para evitar mezclar toda la lógica en un solo archivo:

- `app.py`: punto de entrada de la aplicación.
- `auth.py`: contiene la lógica de autenticación y gestión de acceso.
- `chat.py`: concentra la funcionalidad del chat y la comunicación en tiempo real.
- `models.py`: define los modelos de datos y su relación con la base de datos.
- `templates/`: vistas HTML renderizadas por Flask.
- `static/`: estilos y scripts del frontend.

La comunicación en tiempo real se realiza mediante **Socket.IO / WebSockets**, lo que permite que los mensajes aparezcan sin recargar la página. La persistencia se apoya en **SQLAlchemy** y, según la configuración del proyecto, en **SQLite** como base de datos local.

## Funcionalidades principales

- Registro de usuarios.
- Inicio y cierre de sesión.
- Chat en tiempo real.
- Gestión de contactos.
- Envío de imágenes.
- Interfaz responsive.
- Estructura modular para facilitar mantenimiento y escalabilidad.

## Tecnologías utilizadas

- Python
- Flask
- Flask-SocketIO
- Flask-Login
- Flask-SQLAlchemy
- HTML5
- CSS3
- JavaScript
- SQLite

## Estructura del proyecto

```txt
Criptalk/
├── app.py
├── auth.py
├── chat.py
├── models.py
├── templates/
│   ├── base.html
│   ├── chat.html
│   ├── login.html
│   └── register.html
├── static/
│   ├── style.css
│   └── chat.js
└── requirements.txt
```

## Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/Lord-Golden-777/Criptalk.git
cd Criptalk
```

### 2. Crea un entorno virtual

```bash
python -m venv venv
```

Activación:

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecuta la aplicación

```bash
python app.py
```

## Uso

1. Abre la aplicación en tu navegador.
2. Crea una cuenta o inicia sesión.
3. Entra al chat.
4. Envía mensajes y, si está habilitado en tu implementación, imágenes.
5. La interfaz actualiza el contenido en tiempo real sin necesidad de recargar la página.

## Arquitectura del proyecto

CripTalk sigue una separación bastante sana entre capas:

- **Capa de presentación**: HTML, CSS y JavaScript.
- **Capa de aplicación**: rutas, eventos y control del flujo.
- **Capa de datos**: modelos y persistencia con SQLAlchemy.
- **Tiempo real**: Socket.IO para eventos instantáneos.

Ese enfoque hace que el proyecto sea más legible, más fácil de depurar y mucho más simple de extender.

## Qué se aprende con este proyecto

Este repositorio sirve para practicar:

- autenticación de usuarios,
- diseño de aplicaciones web con Flask,
- integración de frontend y backend,
- comunicación en tiempo real,
- organización de código en módulos,
- persistencia de datos con SQLAlchemy,
- manejo básico de una interfaz de chat.

## Mejoras futuras

- chats grupales,
- cifrado de extremo a extremo,
- videollamadas,
- sistema de notificaciones,
- modo oscuro avanzado,
- despliegue en la nube,
- mejoras de seguridad y optimización.

## Contribuciones

Las contribuciones son bienvenidas.

Si quieres mejorar el proyecto:

1. Haz un fork del repositorio.
2. Crea una rama para tu cambio.
3. Realiza tus modificaciones.
4. Abre un Pull Request con una explicación clara.

## Licencia

Este proyecto se distribuye bajo licencia MIT.

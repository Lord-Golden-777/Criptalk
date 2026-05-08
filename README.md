💬 Criptalk

Una plataforma de mensajería moderna, segura y de alta velocidad.Construida con Flask y comunicación bidireccional mediante WebSockets.Descripción • Características • Tecnologías • Instalación • Seguridad📋 Sobre el ProyectoCriptalk es una solución de mensajería instantánea diseñada para ofrecer una experiencia de usuario fluida y privada. Permite la interacción en tiempo real a través de canales individuales o grupales, integrando un sistema de búsqueda eficiente y un esquema de contactos basado en identificadores únicos para maximizar la privacidad.Es ideal como base para sistemas de comunicación corporativa, plataformas educativas o aplicaciones sociales personalizadas.✨ Características Principales⚡ Comunicación Real-Time: Mensajería instantánea sin latencia mediante WebSockets.👥 Gestión de Grupos: Creación y administración de salas de chat multiusuario.🖼️ Multimedia Ready: Soporte optimizado para envío de imágenes (PNG, JPG, GIF, WebP).🔍 Búsqueda Indexada: Localización rápida de mensajes específicos dentro de cualquier hilo de conversación.🆔 Identificadores Únicos: Sistema de agregación de contactos mediante códigos de 5 caracteres, evitando la exposición de correos electrónicos.📱 Diseño Adaptativo: Interfaz mobile-first desarrollada con CSS moderno para cualquier dispositivo.🛠️ Stack TecnológicoComponenteHerramientas UtilizadasBackendPython 3.8+, Flask FrameworkTiempo RealFlask-SocketIO (Engine.IO)PersistenciaSQLAlchemy (ORM), SQLite / PostgreSQLFrontendHTML5, CSS3 (Custom Properties), Vanilla JavaScriptSeguridadWerkzeug (Hashing), Flask-Login📦 Guía de InstalaciónSigue estos pasos para desplegar un entorno de desarrollo local.1. Clonar el repositorioBashgit clone https://github.com/Lord-Golden-777/Criptalk.git
cd "Criptalk/Proyecto Final"
2. Configurar Entorno VirtualBash# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
3. Instalación de DependenciasBashpip install --upgrade pip
pip install -r requirements.txt
4. InicializaciónBashpython app.py
Accede a través de: http://localhost:5000📁 Estructura del EcosistemaPlaintext├── app.py              # Entry point y configuración del servidor
├── ext.py              # Inicialización de extensiones (DB, Login, Sockets)
├── models.py           # Definición de esquemas de base de datos
├── auth.py             # Lógica de autenticación y sesiones
├── chat.py             # Gestión de eventos de WebSocket y rutas de chat
├── static/             # Assets: CSS, JS e imágenes de usuario
└── templates/          # Vistas renderizadas (Jinja2)
🔐 Arquitectura de SeguridadCriptalk implementa múltiples capas de protección para garantizar la integridad de los datos:Protección de Identidad: El sistema de códigos únicos minimiza el spam y la recolección de datos sensibles.Cifrado de Credenciales: Uso de algoritmos de hashing de última generación para el almacenamiento de contraseñas.Seguridad en Carga de Archivos: Validación rigurosa de tipos MIME y saneamiento de nombres de archivo.Defensa CSRF: Protección activa contra ataques de falsificación de solicitudes en todos los formularios.🤝 Contribuciones y Mejora Continua¡El proyecto está abierto a nuevas ideas! Áreas prioritarias para futuras versiones:[ ] Implementación de cifrado End-to-End (E2EE).[ ] Notificaciones Push nativas.[ ] Modo Oscuro dinámico basado en preferencias del sistema.[ ] Soporte para transferencia de documentos (PDF, DOCX).Para contribuir:Haz un Fork del proyecto.Crea una rama para tu característica: git checkout -b feature/AmazingFeature.Realiza un Commit: git commit -m 'Add AmazingFeature'.Haz un Push: git push origin feature/AmazingFeature.Abre un Pull Request.📄 LicenciaEste software se distribuye bajo la licencia MIT. Consulta el archivo LICENSE para más información.Desarrollado con ❤️ por Adrian

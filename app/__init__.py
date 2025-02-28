from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    # Configuración de la clave secreta
    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'

    # Configuración de las carpetas de carga y salida
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
    app.config['OUTPUT_FOLDER'] = os.path.join(app.root_path, 'outputs')
    app.config['ALLOWED_EXTENSIONS'] = {'kml'}

    # Crear carpetas si no existen
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['OUTPUT_FOLDER']):
        os.makedirs(app.config['OUTPUT_FOLDER'])

    # Registrar rutas
    from .routes import main_routes
    app.register_blueprint(main_routes)

    return app
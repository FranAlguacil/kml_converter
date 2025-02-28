from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, current_app
from .utils import allowed_file, kml_to_shp, zip_files
import os

main_routes = Blueprint('main', __name__)

@main_routes.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verificar si se subieron archivos
        if 'files' not in request.files:
            flash('No se seleccionaron archivos', 'error')
            return redirect(request.url)

        files = request.files.getlist('files')
        if not files or all(file.filename == '' for file in files):
            flash('No se seleccionaron archivos', 'error')
            return redirect(request.url)

        # Procesar archivos
        output_files = []
        for file in files:
            if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
                filename = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
                generated_files = kml_to_shp(filename, current_app.config['OUTPUT_FOLDER'])
                if generated_files:
                    # Comprimir los archivos generados en un ZIP
                    zip_name = f"{os.path.splitext(file.filename)[0]}.zip"
                    zip_path = zip_files(current_app.config['OUTPUT_FOLDER'], generated_files, zip_name)
                    output_files.append(zip_name)  # Solo el nombre del archivo ZIP
            else:
                flash(f'Archivo no permitido: {file.filename}', 'error')

        if output_files:
            flash('Conversión completada con éxito', 'success')
            return render_template('index.html', output_files=output_files)

    return render_template('index.html')

@main_routes.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(current_app.config['OUTPUT_FOLDER'], filename)
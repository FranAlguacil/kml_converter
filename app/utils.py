import os
import geopandas as gpd
import zipfile

def allowed_file(filename, allowed_extensions):
    """
    Verifica si un archivo tiene una extensión permitida.
    :param filename: Nombre del archivo.
    :param allowed_extensions: Lista de extensiones permitidas.
    :return: True si la extensión es permitida, False en caso contrario.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def kml_to_shp(kml_file, output_folder):
    """
    Convierte un archivo KML a SHP y devuelve una lista de archivos generados.
    :param kml_file: Ruta del archivo KML.
    :param output_folder: Carpeta de salida para los archivos SHP.
    :return: Lista de archivos generados.
    """
    try:
        base_name = os.path.splitext(os.path.basename(kml_file))[0]
        shp_file = os.path.join(output_folder, f"{base_name}.shp")

        gdf = gpd.read_file(kml_file, driver='KML')
        gdf.to_file(shp_file, driver='ESRI Shapefile')

        # Obtener todos los archivos generados
        generated_files = [
            f for f in os.listdir(output_folder)
            if f.startswith(base_name) and f.endswith(('.shp', '.shx', '.dbf', '.prj', '.cpg'))
        ]

        print(f"Archivos generados: {generated_files}")  # Mensaje de depuración
        return generated_files
    except Exception as e:
        print(f"Error en la conversión de {kml_file}: {e}")  # Mensaje de error
        return None

def zip_files(output_folder, files, zip_name):
    """
    Comprime una lista de archivos en un archivo ZIP.
    :param output_folder: Carpeta donde se encuentran los archivos.
    :param files: Lista de nombres de archivos.
    :param zip_name: Nombre del archivo ZIP.
    :return: Ruta del archivo ZIP generado.
    """
    zip_path = os.path.join(output_folder, zip_name)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            file_path = os.path.join(output_folder, file)
            zipf.write(file_path, arcname=file)
    return zip_path
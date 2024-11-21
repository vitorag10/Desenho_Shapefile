from flask import Flask, request, send_from_directory, jsonify
import os
import fiona
from shapely.geometry import LineString
from fiona.crs import from_epsg

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './outputs'

# Garantir que as pastas de upload e output existam
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    
    # Verifica se os dados foram recebidos corretamente
    if not data or 'coordinates' not in data or 'filename' not in data:
        return jsonify({"error": "Dados incompletos fornecidos"}), 400

    coordinates = data['coordinates']
    filename = data['filename']
    
    if not filename.endswith('.shp'):
        filename += '.shp'

    shapefile_path = os.path.join(OUTPUT_FOLDER, filename)

    schema = {
        'geometry': 'LineString',
        'properties': {'id': 'int'},
    }

    with fiona.open(shapefile_path, 'w', driver='ESRI Shapefile', schema=schema, crs=from_epsg(4326)) as shp:
        line = LineString([(lon, lat) for lat, lon in coordinates])
        shp.write({
            'geometry': {
                'type': 'LineString',
                'coordinates': list(line.coords),
            },
            'properties': {'id': 1},
        })

    return jsonify({"shapefilePath": filename}), 200


@app.route('/download/<filename>')
def download(filename):
    # Corrigir para o diretório correto, sem caminho absoluto
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

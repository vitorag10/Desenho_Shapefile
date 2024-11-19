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
    if not data or 'coordinates' not in data:
        return jsonify({"error": "Nenhuma coordenada fornecida"}), 400

    coordinates = data['coordinates']  # Lista de coordenadas [[lat1, lon1], [lat2, lon2], ...]

    # Definindo o nome base para o shapefile
    shapefile_base = 'drawing'
    shapefile_path = os.path.join(OUTPUT_FOLDER, shapefile_base + '.shp')

    # Criando o schema do shapefile para armazenar dados do tipo LineString
    schema = {
        'geometry': 'LineString',
        'properties': {'id': 'int'},
    }

    # Criando o shapefile
    with fiona.open(shapefile_path, 'w', driver='ESRI Shapefile', schema=schema, crs=from_epsg(4326)) as shp:
        line = LineString([(lon, lat) for lat, lon in coordinates])  # Linha a partir das coordenadas
        shp.write({
            'geometry': {
                'type': 'LineString',
                'coordinates': list(line.coords),
            },
            'properties': {'id': 1},
        })

    # Retorna o caminho do shapefile gerado
    return jsonify({"shapefilePath": shapefile_path}), 200

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
import mysql.connector
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Configuration Swagger
SWAGGER_URL = '/docs'  # L'URL pour accéder à la doc
API_URL = '/static/swagger.json'  # Où se trouve le fichier JSON qu'on a créé

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "InfraMusicStore API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Route pour servir le fichier swagger.json (nécessaire pour que l'UI le trouve)
@app.route('/static/swagger.json')
def swagger_json():
    return app.send_static_file('swagger.json')

# Configuration de la base de données
def get_db_connection():
    # Si on est dans Docker, le host est 'db', sinon c'est 'localhost'
    db_host = os.getenv('DB_HOST', 'localhost')
    
    connection = mysql.connector.connect(
        host=db_host,
        user='user',
        password='password',
        database='chinook',
        port=3306
    )
    return connection

@app.route('/')
def home():
    return jsonify({"message": "Bienvenue sur l'API InfraMusicStore !"})

# --- CRUD ARTIST (Exemple complet) ---

# 1. LIRE TOUS LES ARTISTES (GET)
@app.route('/api/artists', methods=['GET'])
def get_artists():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM Artist LIMIT 50') # On limite à 50 pour l'exemple
        artists = cursor.fetchall()
        conn.close()
        return jsonify(artists)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. LIRE UN SEUL ARTISTE (GET BY ID)
@app.route('/api/artists/<int:id>', methods=['GET'])
def get_artist(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Artist WHERE ArtistId = %s', (id,))
    artist = cursor.fetchone()
    conn.close()
    if artist:
        return jsonify(artist)
    return jsonify({"error": "Artiste non trouvé"}), 404

# 3. CRÉER UN ARTISTE (POST)
@app.route('/api/artists', methods=['POST'])
def create_artist():
    new_artist = request.get_json()
    name = new_artist.get('Name')
    
    if not name:
        return jsonify({"error": "Le nom est obligatoire"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Artist (Name) VALUES (%s)', (name,))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return jsonify({"id": new_id, "Name": name}), 201

# 4. SUPPRIMER UN ARTISTE (DELETE)
@app.route('/api/artists/<int:id>', methods=['DELETE'])
def delete_artist(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Artist WHERE ArtistId = %s', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Artiste supprimé avec succès"}), 200

if __name__ == '__main__':
    # On écoute sur toutes les interfaces (0.0.0.0) pour que Docker puisse y accéder plus tard
    app.run(host='0.0.0.0', port=5000, debug=True)
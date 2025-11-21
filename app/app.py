from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
import mysql.connector
import os
from dotenv import load_dotenv

# Charger les variables d'environnement (.env en local)
load_dotenv()

app = Flask(__name__)

# ───────────────────────── Swagger UI ─────────────────────────
SWAGGER_URL = "/docs"
API_URL = "/static/swagger.json"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "InfraMusicStore API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route("/static/swagger.json")
def swagger_json():
    """Retourne le fichier swagger.json situé dans /app/static."""
    return app.send_static_file("swagger.json")


# ───────────────────────── Base de données ─────────────────────────
def get_db_connection():
    """
    Crée une connexion MySQL en utilisant uniquement les variables d'environnement.
    En Docker : valeurs fournies par docker-compose
    En local : valeurs définies dans .env
    """
    db_config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "user": os.getenv("DB_USER", "user"),
        "password": os.getenv("DB_PASSWORD", "password"),
        "database": os.getenv("DB_NAME", "chinook"),
    }
    return mysql.connector.connect(**db_config)


@app.route("/")
def home():
    return jsonify({"message": "Bienvenue sur l'API InfraMusicStore !"})

# =================================================================
#  ARTISTS CRUD
# =================================================================

@app.route("/api/artists", methods=["GET"])
def get_artists():
    """Récupérer tous les artistes (limités à 100)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Artist LIMIT 100")
        artists = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(artists), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/artists/<int:artist_id>", methods=["GET"])
def get_artist(artist_id):
    """Récupérer un artiste par son ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Artist WHERE ArtistId = %s", (artist_id,))
        artist = cursor.fetchone()
        cursor.close()
        conn.close()

        if artist:
            return jsonify(artist), 200
        return jsonify({"error": "Artiste non trouvé"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/artists", methods=["POST"])
def create_artist():
    """Créer un nouvel artiste."""
    data = request.get_json() or {}
    name = data.get("Name") or data.get("name")

    if not name:
        return jsonify({"error": "Le champ 'Name' est obligatoire"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Artist (Name) VALUES (%s)", (name,))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"ArtistId": new_id, "Name": name}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/artists/<int:artist_id>", methods=["PUT"])
def update_artist(artist_id):
    """Mettre à jour un artiste (son nom)."""
    data = request.get_json() or {}
    name = data.get("Name") or data.get("name")

    if not name:
        return jsonify({"error": "Le champ 'Name' est obligatoire"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Artist SET Name = %s WHERE ArtistId = %s", (name, artist_id))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"error": "Artiste non trouvé"}), 404

        return jsonify({"ArtistId": artist_id, "Name": name}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/artists/<int:artist_id>", methods=["DELETE"])
def delete_artist(artist_id):
    """Supprimer un artiste."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Artist WHERE ArtistId = %s", (artist_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"error": "Artiste non trouvé"}), 404

        return jsonify({"message": "Artiste supprimé avec succès"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =================================================================
#  ALBUMS CRUD
# =================================================================

@app.route("/api/albums", methods=["GET"])
def get_albums():
    """Récupérer tous les albums."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Album LIMIT 100")
        albums = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(albums), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/albums/<int:album_id>", methods=["GET"])
def get_album(album_id):
    """Récupérer un album par ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Album WHERE AlbumId = %s", (album_id,))
        album = cursor.fetchone()
        cursor.close()
        conn.close()

        if album:
            return jsonify(album), 200
        return jsonify({"error": "Album non trouvé"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/albums", methods=["POST"])
def create_album():
    """Créer un album."""
    data = request.get_json() or {}
    title = data.get("Title") or data.get("title")
    artist_id = data.get("ArtistId") or data.get("artist_id")

    if not title or not artist_id:
        return jsonify({"error": "Les champs 'Title' et 'ArtistId' sont obligatoires"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Album (Title, ArtistId) VALUES (%s, %s)",
            (title, artist_id),
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"AlbumId": new_id, "Title": title, "ArtistId": artist_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/albums/<int:album_id>", methods=["PUT"])
def update_album(album_id):
    """Mettre à jour un album."""
    data = request.get_json() or {}
    title = data.get("Title") or data.get("title")
    artist_id = data.get("ArtistId") or data.get("artist_id")

    if not title or not artist_id:
        return jsonify({"error": "Les champs 'Title' et 'ArtistId' sont obligatoires"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Album SET Title = %s, ArtistId = %s WHERE AlbumId = %s",
            (title, artist_id, album_id),
        )
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"error": "Album non trouvé"}), 404

        return jsonify({"AlbumId": album_id, "Title": title, "ArtistId": artist_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/albums/<int:album_id>", methods=["DELETE"])
def delete_album(album_id):
    """Supprimer un album."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Album WHERE AlbumId = %s", (album_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"error": "Album non trouvé"}), 404

        return jsonify({"message": "Album supprimé avec succès"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =================================================================
#  GENRES CRUD
# =================================================================

@app.route("/api/genres", methods=["GET"])
def get_genres():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Genre LIMIT 100")
        genres = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(genres), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/genres/<int:genre_id>", methods=["GET"])
def get_genre(genre_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Genre WHERE GenreId = %s", (genre_id,))
        genre = cursor.fetchone()
        cursor.close()
        conn.close()

        if genre:
            return jsonify(genre), 200
        return jsonify({"error": "Genre non trouvé"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/genres", methods=["POST"])
def create_genre():
    data = request.get_json() or {}
    name = data.get("Name") or data.get("name")

    if not name:
        return jsonify({"error": "Le champ 'Name' est obligatoire"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Genre (Name) VALUES (%s)", (name,))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({"GenreId": new_id, "Name": name}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/genres/<int:genre_id>", methods=["PUT"])
def update_genre(genre_id):
    data = request.get_json() or {}
    name = data.get("Name") or data.get("name")

    if not name:
        return jsonify({"error": "Le champ 'Name' est obligatoire"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Genre SET Name = %s WHERE GenreId = %s", (name, genre_id))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"error": "Genre non trouvé"}), 404

        return jsonify({"GenreId": genre_id, "Name": name}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/genres/<int:genre_id>", methods=["DELETE"])
def delete_genre(genre_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Genre WHERE GenreId = %s", (genre_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"error": "Genre non trouvé"}), 404

        return jsonify({"message": "Genre supprimé avec succès"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =================================================================
#  TRACKS CRUD
# =================================================================

@app.route("/api/tracks", methods=["GET"])
def get_tracks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Track LIMIT 100")
        tracks = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(tracks), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tracks/<int:track_id>", methods=["GET"])
def get_track(track_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Track WHERE TrackId = %s", (track_id,))
        track = cursor.fetchone()
        cursor.close()
        conn.close()

        if track:
            return jsonify(track), 200
        return jsonify({"error": "Piste non trouvée"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tracks", methods=["POST"])
def create_track():
    data = request.get_json() or {}
    required = ["Name", "AlbumId", "MediaTypeId", "GenreId", "Milliseconds", "UnitPrice"]

    if any(field not in data for field in required):
        return jsonify({"error": f"Champs obligatoires : {', '.join(required)}"}), 400

    name = data["Name"]
    album_id = data["AlbumId"]
    media_type_id = data["MediaTypeId"]
    genre_id = data["GenreId"]
    composer = data.get("Composer")
    milliseconds = data["Milliseconds"]
    bytes_ = data.get("Bytes")
    unit_price = data["UnitPrice"]

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Track
            (Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (name, album_id, media_type_id, genre_id, composer, milliseconds, bytes_, unit_price),
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()

        data["TrackId"] = new_id
        return jsonify(data), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tracks/<int:track_id>", methods=["PUT"])
def update_track(track_id):
    data = request.get_json() or {}
    # On autorise la mise à jour partielle
    fields = []
    values = []

    for column in ["Name", "AlbumId", "MediaTypeId", "GenreId", "Composer", "Milliseconds", "Bytes", "UnitPrice"]:
        if column in data:
            fields.append(f"{column} = %s")
            values.append(data[column])

    if not fields:
        return jsonify({"error": "Aucun champ à mettre à jour"}), 400

    values.append(track_id)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = f"UPDATE Track SET {', '.join(fields)} WHERE TrackId = %s"
        cursor.execute(query, tuple(values))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"error": "Piste non trouvée"}), 404

        return jsonify({"message": "Piste mise à jour avec succès"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/tracks/<int:track_id>", methods=["DELETE"])
def delete_track(track_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Track WHERE TrackId = %s", (track_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({"error": "Piste non trouvée"}), 404

        return jsonify({"message": "Piste supprimée avec succès"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ───────────────────────── Entrypoint ─────────────────────────
if __name__ == "__main__":
    # 0.0.0.0 pour être accessible depuis Docker
    app.run(host="0.0.0.0", port=5000, debug=True)

import mysql.connector
from faker import Faker
import random

# ≡ 1. Connexion à la base
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",    # Mets ton mot de passe si besoin !
    database="chinook"
)
cursor = conn.cursor()
fake = Faker()

# ≡ 2. Insertion dans Artist (20 lignes)
artist_ids = []
for _ in range(20):
    name = fake.name()
    cursor.execute("INSERT INTO Artist (Name) VALUES (%s)", (name,))
    artist_ids.append(cursor.lastrowid)
conn.commit()

# ≡ 3. Insertion dans Genre (5 genres aléatoires)
genre_ids = []
for _ in range(5):
    genre_name = fake.word().capitalize()
    cursor.execute("INSERT INTO Genre (Name) VALUES (%s)", (genre_name,))
    genre_ids.append(cursor.lastrowid)
conn.commit()

# ≡ 4. Insertion dans MediaType (3 mediatypes)
media_ids = []
for ext in ["MP3", "AAC", "WAV"]:
    cursor.execute("INSERT INTO MediaType (Name) VALUES (%s)", (ext,))
    media_ids.append(cursor.lastrowid)
conn.commit()

# ≡ 5. Insertion dans Album (20 albums, chaque album pour un artiste random)
album_ids = []
for _ in range(20):
    title = fake.sentence(nb_words=3)
    artist_id = random.choice(artist_ids)
    cursor.execute("INSERT INTO Album (Title, ArtistId) VALUES (%s, %s)", (title, artist_id))
    album_ids.append(cursor.lastrowid)
conn.commit()

# ≡ 6. Insertion dans Track (20 tracks, FK vers Album, MediaType, Genre)
track_ids = []
for _ in range(20):
    name = fake.sentence(nb_words=4)
    album_id = random.choice(album_ids)
    genre_id = random.choice(genre_ids)
    media_id = random.choice(media_ids)
    composer = fake.name()
    ms = random.randint(180000, 420000)
    bytes_ = random.randint(1000000, 9000000)
    price = round(random.uniform(0.99, 2.99), 2)
    cursor.execute("""
        INSERT INTO Track (Name, AlbumId, GenreId, MediaTypeId, Composer, Milliseconds, Bytes, UnitPrice)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, album_id, genre_id, media_id, composer, ms, bytes_, price))
    track_ids.append(cursor.lastrowid)
conn.commit()

# ≡ 7. Insertion dans Playlist (20 playlists)
playlist_ids = []
for _ in range(20):
    name = fake.word().capitalize() + " Playlist"
    cursor.execute("INSERT INTO Playlist (Name) VALUES (%s)", (name,))
    playlist_ids.append(cursor.lastrowid)
conn.commit()

# ≡ 8. Insertion dans PlaylistTrack (associations N-N)
for playlist_id in playlist_ids:
    tracks_sample = random.sample(track_ids, k=random.randint(5, 10))
    for track_id in tracks_sample:
        cursor.execute("INSERT INTO PlaylistTrack (PlaylistId, TrackId) VALUES (%s, %s)", (playlist_id, track_id))
conn.commit()

# ≡ 9. Fin et fermeture
cursor.close()
conn.close()
print("✓ Données aléatoires programmatiquement insérées dans toutes les tables !")

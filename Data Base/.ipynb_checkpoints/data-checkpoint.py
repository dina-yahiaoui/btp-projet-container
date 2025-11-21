# =====================================================
# Script d'insertion de données de test dans Chinook
# Utilise mysql-connector-python pour la connexion
# =====================================================

import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import random

# =====================================================
# 1. CONNEXION À LA BASE DE DONNÉES
# =====================================================

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",          # Adresse du serveur (localhost)
        user="root",                # Utilisateur MySQL
        password="",                # Mot de passe (laisse vide si pas de password)
        database="projet_chinook"          # Nom de la base
    )
    
    if conn.is_connected():
        cursor = conn.cursor()
        print("✓ Connexion à la base de données réussie !")
    
except Error as e:
    print(f"✗ Erreur de connexion : {e}")
    exit()

# =====================================================
# 2. LISTES DE DONNÉES DE TEST
# =====================================================

# Noms d'artistes (20)
artists_data = [
    "The Beatles", "Led Zeppelin", "Pink Floyd", "Queen", "The Rolling Stones",
    "AC/DC", "Metallica", "Nirvana", "Radiohead", "Coldplay",
    "U2", "The Doors", "Jimi Hendrix", "Bob Dylan", "David Bowie",
    "Elton John", "Michael Jackson", "Prince", "Madonna", "Whitney Houston"
]

# Titres d'albums (20)
albums_data = [
    "Abbey Road", "Let It Be", "Led Zeppelin IV", "Physical Graffiti",
    "The Dark Side of the Moon", "Wish You Were Here", "A Night at the Opera",
    "News of the World", "Sticky Fingers", "Exile on Main St.",
    "Back in Black", "Highway to Hell", "Master of Puppets", "Ride the Lightning",
    "Nevermind", "In Utero", "OK Computer", "Kid A", "Parachutes",
    "A Rush of Blood to the Head"
]

# Noms de pistes (20)
tracks_data = [
    "Come Together", "Something", "Dear Prudence", "Norwegian Wood",
    "Blackbird", "While My Guitar Gently Weeps", "Strawberry Fields Forever",
    "Penny Lane", "Revolution", "Lady Madonna",
    "Back in Black", "Highway to Hell", "Shot Down in Flames", "What Do You Do for Money Honey",
    "Whole Lotta Rosie", "You Shook Me All Night Long", "Let Me Put My Love Into You",
    "Problem Child", "Rocker", "Hell Ain't a Bad Place to Be"
]

# Noms de playlists (20)
playlists_data = [
    "Rock Classics", "80s Metal", "British Invasion", "Grunge Essentials",
    "Pink Floyd Journey", "Queen Anthology", "Beatles Best", "Zeppelin Classics",
    "Nirvana Collection", "Modern Classics", "Progressive Rock", "Hard Rock",
    "Rock Legends", "Greatest Hits", "My Favorites", "Workout Mix",
    "Chill Vibes", "Party Playlist", "Road Trip", "Study Music"
]

# =====================================================
# 3. INSERTION DES DONNÉES
# =====================================================

try:
    # --- INSERTION DANS ARTIST (20 artistes) ---
    print("\n📝 Insertion des artistes...")
    for artist_name in artists_data:
        query = "INSERT INTO Artist (Name) VALUES (%s)"
        cursor.execute(query, (artist_name,))
    conn.commit()
    print(f"✓ {len(artists_data)} artistes insérés")
    
    # --- INSERTION DANS GENRE (5 genres) ---
    print("\n📝 Insertion des genres...")
    genres = ["Rock", "Metal", "Pop", "Blues", "Alternative"]
    for genre_name in genres:
        query = "INSERT INTO Genre (Name) VALUES (%s)"
        cursor.execute(query, (genre_name,))
    conn.commit()
    print(f"✓ {len(genres)} genres insérés")
    
    # --- INSERTION DANS MEDIATYPE (3 formats) ---
    print("\n📝 Insertion des types de média...")
    mediatypes = ["MPEG audio file", "AAC audio file", "WAV audio file"]
    for mediatype_name in mediatypes:
        query = "INSERT INTO MediaType (Name) VALUES (%s)"
        cursor.execute(query, (mediatype_name,))
    conn.commit()
    print(f"✓ {len(mediatypes)} types de média insérés")
    
    # --- INSERTION DANS ALBUM (20 albums) ---
    print("\n📝 Insertion des albums...")
    for i, album_title in enumerate(albums_data):
        artist_id = (i % 20) + 1  # Associe chaque album à un artiste (1-20)
        query = "INSERT INTO Album (Title, ArtistId) VALUES (%s, %s)"
        cursor.execute(query, (album_title, artist_id))
    conn.commit()
    print(f"✓ {len(albums_data)} albums insérés")
    
    # --- INSERTION DANS TRACK (20 pistes) ---
    print("\n📝 Insertion des pistes...")
    for i, track_name in enumerate(tracks_data):
        album_id = (i % 20) + 1       # Associe à un album (1-20)
        genre_id = (i % 5) + 1        # Associe à un genre (1-5)
        mediatype_id = (i % 3) + 1    # Associe à un type média (1-3)
        milliseconds = random.randint(180000, 420000)  # 3-7 minutes
        unit_price = round(random.uniform(0.99, 1.99), 2)
        
        query = """INSERT INTO Track (Name, AlbumId, GenreId, MediaTypeId, Milliseconds, UnitPrice)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (track_name, album_id, genre_id, mediatype_id, milliseconds, unit_price))
    conn.commit()
    print(f"✓ {len(tracks_data)} pistes insérées")
    
    # --- INSERTION DANS PLAYLIST (20 playlists) ---
    print("\n📝 Insertion des playlists...")
    for playlist_name in playlists_data:
        query = "INSERT INTO Playlist (Name) VALUES (%s)"
        cursor.execute(query, (playlist_name,))
    conn.commit()
    print(f"✓ {len(playlists_data)} playlists insérées")
    
    # --- INSERTION DANS PLAYLISTTRACK (associations N-N) ---
    print("\n📝 Insertion des associations Playlist-Track...")
    associations_count = 0
    for playlist_id in range(1, 21):  # 20 playlists
        # Chaque playlist a 5-10 pistes associées
        nb_tracks = random.randint(5, 10)
        track_ids = random.sample(range(1, 21), nb_tracks)
        
        for track_id in track_ids:
            query = "INSERT INTO PlaylistTrack (PlaylistId, TrackId) VALUES (%s, %s)"
            cursor.execute(query, (playlist_id, track_id))
            associations_count += 1
    
    conn.commit()
    print(f"✓ {associations_count} associations Playlist-Track insérées")
    
    # --- RÉSUMÉ FINAL ---
    print("\n" + "="*50)
    print("✓ INSERTION COMPLÈTE !")
    print("="*50)
    print(f"✓ 20 Artistes")
    print(f"✓ 5 Genres")
    print(f"✓ 3 Types de média")
    print(f"✓ 20 Albums")
    print(f"✓ 20 Pistes")
    print(f"✓ 20 Playlists")
    print(f"✓ {associations_count} Associations Playlist-Track")
    print("="*50)

except Error as e:
    print(f"✗ Erreur lors de l'insertion : {e}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()
    print("\n✓ Connexion fermée")

USE projet_chinook;

CREATE TABLE Artist (
    ArtistId INT NOT NULL AUTO_INCREMENT,
    Name NVARCHAR(120),
    CONSTRAINT PK_Artist PRIMARY KEY (ArtistId)
);

CREATE TABLE Album (
    AlbumId INT NOT NULL AUTO_INCREMENT,
    Title NVARCHAR(160) NOT NULL,
    ArtistId INT NOT NULL,
    CONSTRAINT PK_Album PRIMARY KEY (AlbumId)
);

CREATE TABLE Genre (
    GenreId INT NOT NULL AUTO_INCREMENT,
    Name NVARCHAR(120),
    CONSTRAINT PK_Genre PRIMARY KEY (GenreId)
);

CREATE TABLE MediaType (
    MediaTypeId INT NOT NULL AUTO_INCREMENT,
    Name NVARCHAR(120),
    CONSTRAINT PK_MediaType PRIMARY KEY (MediaTypeId)
);

CREATE TABLE Track (
    TrackId INT NOT NULL AUTO_INCREMENT,
    Name NVARCHAR(200) NOT NULL,
    AlbumId INT,
    MediaTypeId INT NOT NULL,
    GenreId INT,
    Composer NVARCHAR(220),
    Milliseconds INT NOT NULL,
    Bytes INT,
    UnitPrice NUMERIC(10,2) NOT NULL,
    CONSTRAINT PK_Track PRIMARY KEY (TrackId)
);

CREATE TABLE Playlist (
    PlaylistId INT NOT NULL AUTO_INCREMENT,
    Name NVARCHAR(120),
    CONSTRAINT PK_Playlist PRIMARY KEY (PlaylistId)
);

CREATE TABLE PlaylistTrack (
    PlaylistId INT NOT NULL,
    TrackId INT NOT NULL,
    CONSTRAINT PK_PlaylistTrack PRIMARY KEY (PlaylistId, TrackId)
);

-- Creation des alter table pour les FK

ALTER TABLE Album
    ADD CONSTRAINT FK_AlbumArtistId FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId);

ALTER TABLE Track
    ADD CONSTRAINT FK_TrackAlbumId FOREIGN KEY (AlbumId) REFERENCES Album(AlbumId);

ALTER TABLE Track
    ADD CONSTRAINT FK_TrackGenreId FOREIGN KEY (GenreId) REFERENCES Genre(GenreId);

ALTER TABLE Track
    ADD CONSTRAINT FK_TrackMediaTypeId FOREIGN KEY (MediaTypeId) REFERENCES MediaType(MediaTypeId);

ALTER TABLE PlaylistTrack
    ADD CONSTRAINT FK_PlaylistTrackPlaylistId FOREIGN KEY (PlaylistId) REFERENCES Playlist(PlaylistId);

ALTER TABLE PlaylistTrack
    ADD CONSTRAINT FK_PlaylistTrackTrackId FOREIGN KEY (TrackId) REFERENCES Track(TrackId);

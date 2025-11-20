-- db_scripts/init.sql

CREATE TABLE IF NOT EXISTS Artist (
    ArtistId INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(120)
);

CREATE TABLE IF NOT EXISTS Album (
    AlbumId INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(160) NOT NULL,
    ArtistId INT NOT NULL,
    FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId)
);

CREATE TABLE IF NOT EXISTS MediaType (
    MediaTypeId INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(120)
);

CREATE TABLE IF NOT EXISTS Genre (
    GenreId INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(120)
);

CREATE TABLE IF NOT EXISTS Track (
    TrackId INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(200) NOT NULL,
    AlbumId INT,
    MediaTypeId INT NOT NULL,
    GenreId INT,
    Composer VARCHAR(220),
    Milliseconds INT NOT NULL,
    Bytes INT,
    UnitPrice DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (AlbumId) REFERENCES Album(AlbumId),
    FOREIGN KEY (MediaTypeId) REFERENCES MediaType(MediaTypeId),
    FOREIGN KEY (GenreId) REFERENCES Genre(GenreId)
);

-- DONNÉES DE TEST (SEED) OBLIGATOIRES 
INSERT INTO Artist (Name) VALUES ('AC/DC'), ('Accept'), ('Aerosmith');
INSERT INTO Genre (Name) VALUES ('Rock'), ('Jazz'), ('Metal');
INSERT INTO MediaType (Name) VALUES ('MPEG audio file'), ('Protected AAC audio file');

INSERT INTO Album (Title, ArtistId) VALUES 
('For Those About To Rock We Salute You', 1),
('Balls to the Wall', 2),
('Restless and Wild', 2);

INSERT INTO Track (Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice) VALUES
('For Those About To Rock (We Salute You)', 1, 1, 1, 'Angus Young, Malcolm Young, Brian Johnson', 343719, 11170334, 0.99),
('Balls to the Wall', 2, 2, 1, NULL, 342562, 5510424, 0.99),
('Fast As a Shark', 3, 2, 3, 'F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffmann', 230619, 3990994, 0.99);
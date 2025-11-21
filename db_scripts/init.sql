-- db_scripts/init.sql

DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS MediaType;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Artist;

CREATE TABLE IF NOT EXISTS Artist (
    ArtistId INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(120) NOT NULL
);

CREATE TABLE IF NOT EXISTS Album (
    AlbumId INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(160) NOT NULL,
    ArtistId INT NOT NULL,
    FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId)
);

CREATE TABLE IF NOT EXISTS MediaType (
    MediaTypeId INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(120) NOT NULL
);

CREATE TABLE IF NOT EXISTS Genre (
    GenreId INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(120) NOT NULL
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

-- ========= DONNÉES DE TEST =========


-- 8 artistes
INSERT INTO Artist (Name) VALUES
('AC/DC'),
('Accept'),
('Aerosmith'),
('Metallica'),
('Queen'),
('Nirvana'),
('Pink Floyd'),
('The Beatles');

-- 5 genres
INSERT INTO Genre (Name) VALUES
('Rock'),
('Metal'),
('Pop'),
('Grunge'),
('Progressive Rock');

-- 3 types de média
INSERT INTO MediaType (Name) VALUES
('MPEG audio file'),
('Protected AAC audio file'),
('AAC audio file');

-- 10 albums
INSERT INTO Album (Title, ArtistId) VALUES
('For Those About To Rock We Salute You', 1),
('Back in Black', 1),
('Balls to the Wall', 2),
('Restless and Wild', 2),
('Big Ones', 3),
('Master of Puppets', 4),
('A Night at the Opera', 5),
('Nevermind', 6),
('The Dark Side of the Moon', 7),
('Abbey Road', 8);

-- 12 pistes (tracks)
INSERT INTO Track (Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice) VALUES
('For Those About To Rock (We Salute You)', 1, 1, 1, 'Angus Young, Malcolm Young, Brian Johnson', 343719, 11170334, 0.99),
('Put The Finger On You', 1, 1, 1, 'Angus Young, Malcolm Young, Brian Johnson', 205671, 6713456, 0.99),
('Back in Black', 2, 1, 1, 'Angus Young, Malcolm Young, Brian Johnson', 255001, 8450345, 0.99),
('Hells Bells', 2, 1, 1, 'Angus Young, Malcolm Young, Brian Johnson', 312000, 9543021, 0.99),

('Balls to the Wall', 3, 2, 2, NULL, 342562, 5510424, 0.99),
('Fast As a Shark', 4, 2, 2, 'F. Baltes, S. Kaufman, U. Dirkscneider, W. Hoffmann', 230619, 3990994, 0.99),

('Walk This Way', 5, 1, 1, 'Steven Tyler, Joe Perry', 210000, 7000000, 0.99),
('Dream On', 5, 1, 1, 'Steven Tyler', 270000, 9000000, 0.99),

('Master of Puppets', 6, 2, 2, 'Hetfield/Ulrich', 515000, 12000000, 0.99),
('Bohemian Rhapsody', 7, 3, 3, 'Freddie Mercury', 354000, 10000000, 0.99),
('Smells Like Teen Spirit', 8, 1, 4, 'Kurt Cobain', 301000, 9500000, 0.99),
('Time', 9, 3, 5, 'Roger Waters', 413000, 12300000, 0.99);

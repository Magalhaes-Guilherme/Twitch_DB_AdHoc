-- Tabela de Usuarios
CREATE TABLE Usuarios(
	codigo SERIAL PRIMARY KEY,
    user_id VARCHAR(13) UNIQUE NOT NULL,
    login VARCHAR(30) UNIQUE NOT NULL,
    display_name VARCHAR(30) UNIQUE NOT NULL,
    user_type VARCHAR(10),
    broadcaster_type VARCHAR(10),
    description TEXT,
    created_at DATE,
	CHECK(user_type = 'admin' OR user_type = 'global mod' OR user_type = 'staff' OR user_type =  ''),
	CHECK(broadcaster_type = 'affiliate' OR broadcaster_type = 'partner' OR broadcaster_type =  '')
);

-- Tabela de Canais
CREATE TABLE Canais(
	codigo SERIAL PRIMARY KEY,
    channel_id VARCHAR(13) UNIQUE NOT NULL,
    broadcaster_name VARCHAR(30) UNIQUE NOT NULL,
    broadcaster_lang VARCHAR(15),
	FOREIGN KEY (broadcaster_name) REFERENCES Usuarios (display_name)
);

-- Tabela de Categorias (Jogos)
CREATE TABLE Categories(
	codigo SERIAL PRIMARY KEY,
    category_id VARCHAR(13) UNIQUE NOT NULL,
    category_name VARCHAR(80) UNIQUE NOT NULL
);

-- Tabela de Streams
CREATE TABLE Streams(
    codigo SERIAL PRIMARY KEY,
    stream_id VARCHAR(13) UNIQUE,
    broadcaster_name VARCHAR(30) UNIQUE NOT NULL,
    title VARCHAR(140) NOT NULL,
    started_at DATE,
    viewer_count INT,
    stream_lang VARCHAR(15),
    category_name VARCHAR(80),
    FOREIGN KEY (category_name) REFERENCES Categories (category_name),
    FOREIGN KEY (broadcaster_name) REFERENCES Canais (broadcaster_name)
);

-- Tabela de Vídeos
CREATE TABLE Videos(
	codigo SERIAL PRIMARY KEY,
    video_id VARCHAR(13) UNIQUE NOT NULL,
    user_id VARCHAR(13) NOT NULL,
    title VARCHAR(140) NOT NULL,
    created_at TIMESTAMP,
    published_at TIMESTAMP,
    view_count INT,
    video_language VARCHAR(5),
    video_type VARCHAR(15),
    duration VARCHAR(10),
    FOREIGN KEY (user_id) REFERENCES Usuarios(user_id)
);
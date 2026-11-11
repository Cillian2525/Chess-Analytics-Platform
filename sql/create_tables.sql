-- creating games table
CREATE TABLE games (
	game_id INTEGER PRIMARY KEY,
	username VARCHAR(50),
	white_username VARCHAR(50),
	black_username VARCHAR(50),
	white_rating INTEGER,
	black_rating INTEGER,
	result VARCHAR(10),
	date DATE,
	time_control VARCHAR(20),
	time_class VARCHAR(20),
	rated BOOLEAN,
	url TEXT,
	pgn TEXT
);

CREATE TABLE moves (
	game_id INTEGER REFERENCES games(game_id),
	move_number INTEGER,
	colour VARCHAR(5),
	move VARCHAR(10),
	clock_time DOUBLE PRECISION,
	PRIMARY KEY (game_id, move_number, colour)
);
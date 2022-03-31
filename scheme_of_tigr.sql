-- use tigr

CREATE TABLE players(
    id INT AUTO_INCREMENT PRIMARY KEY,
    last_name VARCHAR(100),
    first_name YEAR(4),
    birth_date DATE,
    town_id INT,
    rating INT,
    last_game DATE,
    last_update DATE
);

CREATE TABLE tournaments(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    place varchar(100),
    begin_date DATE,
    end_date DATE,
    komi DOUBLE,
    tours INT,
    rules INT
);

CREATE TABLE participants_of_tournament(
	id INT AUTO_INCREMENT PRIMARY KEY,
    tournament_id INT,
    player_id INT,
    place_in_tournament INT,
    rating_before double,
    rating_after double,
    MM_before double,
    MM_cf DOUBLE,
    BHG_cf DOUBLE,
    BER_cf DOUBLE
);
CREATE TABLE games(
    id INT AUTO_INCREMENT PRIMARY KEY,
    tournament_id INT,
    player1 INT,
    player2 INT,
    color INT,
    game_date DATE,
    tour_num INT,
    board INT
);

CREATE TABLE towns(
	id INT auto_increment primary key,
    town_name varchar(100),
    name_lat varchar(100),
    short_lat varchar(100),
    fed_id int
);
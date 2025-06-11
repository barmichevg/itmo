-- drop
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS disciplines CASCADE;
DROP TABLE IF EXISTS labworks CASCADE;

-- tables
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE disciplines (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL CHECK (char_length(name) > 0),
    practice_hours BIGINT NOT NULL
);

CREATE TABLE labworks (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL CHECK (char_length(name) > 0),
    x INTEGER NOT NULL,
    y REAL NOT NULL CHECK (y <= 654),
    creation_date TIMESTAMP NOT NULL DEFAULT now(),
    minimal_point BIGINT CHECK (minimal_point > 0),
    description TEXT NOT NULL CHECK (char_length(description) <= 5287),
    tuned_in_works INTEGER,
    difficulty TEXT NOT NULL CHECK (difficulty IN ('NORMAL', 'VERY_HARD', 'INSANE', 'HOPELESS')),
    discipline_id INTEGER NOT NULL REFERENCES disciplines(id) ON DELETE CASCADE,
    owner_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

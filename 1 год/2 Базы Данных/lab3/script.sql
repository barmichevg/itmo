DROP TABLE IF EXISTS subjects_origin CASCADE;
DROP TABLE IF EXISTS subjects CASCADE;
DROP TABLE IF EXISTS languages CASCADE;
DROP TABLE IF EXISTS languages_of_subjects CASCADE;
DROP TABLE IF EXISTS analogues_of_languages CASCADE;
DROP TABLE IF EXISTS knowledges CASCADE;
DROP TABLE IF EXISTS knowledges_of_subjects CASCADE;

--build
CREATE TABLE subjects_origin
(
    id SERIAL PRIMARY KEY,
    place TEXT NOT NULL
);

CREATE TABLE subjects
(
    id SERIAL PRIMARY KEY,
    subject_name TEXT NOT NULL,
    origin INTEGER NOT NULL REFERENCES subjects_origin(id),
    origin_place TEXT NOT NULL,
    avg_knowledge_level NUMERIC CHECK (avg_knowledge_level BETWEEN 0 AND 100)
);

CREATE TABLE languages
(
    id SERIAL PRIMARY KEY,
    language_name TEXT NOT NULL,
    difficulty INTEGER NOT NULL CHECK (difficulty BETWEEN 0 AND 100)
);

CREATE TABLE languages_of_subjects
(
    subject_id INTEGER REFERENCES subjects(id) NOT NULL,
    language_id INTEGER REFERENCES languages(id) NOT NULL,
    proficiency_level INTEGER NOT NULL CHECK (proficiency_level BETWEEN 0 AND 100),
    language_name TEXT NOT NULL,

    PRIMARY KEY (subject_id, language_id)
);

CREATE TABLE analogues_of_languages
(
    language_id INTEGER REFERENCES languages(id) NOT NULL,
    analogue_id INTEGER REFERENCES subjects(id) NOT NULL,
    PRIMARY KEY (language_id, analogue_id)
);

CREATE TABLE knowledges
(
    id SERIAL PRIMARY KEY,
    knowledge_name TEXT NOT NULL
);

CREATE TABLE knowledges_of_subjects
(
    subject_id INTEGER REFERENCES subjects(id) NOT NULL,
    knowledge_id INTEGER REFERENCES knowledges(id) NOT NULL,
    level_of_knowledge INTEGER NOT NULL CHECK (level_of_knowledge BETWEEN 0 AND 100),
    PRIMARY KEY (subject_id, knowledge_id)
);

-- 1. Функция для обновления origin_place в subjects
CREATE OR REPLACE FUNCTION update_origin_place()
RETURNS TRIGGER AS $$
BEGIN
    SELECT place INTO NEW.origin_place
    FROM subjects_origin
    WHERE id = NEW.origin;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для subjects
CREATE TRIGGER trg_update_origin_place
BEFORE INSERT OR UPDATE ON subjects
FOR EACH ROW
EXECUTE FUNCTION update_origin_place();

-- 2. Функция для автозаполнения и language_name в languages_of_subjects
CREATE OR REPLACE FUNCTION fill_subject_and_language_names()
RETURNS TRIGGER AS $$
BEGIN
    SELECT language_name INTO NEW.language_name
    FROM languages
    WHERE id = NEW.language_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для languages_of_subjects
CREATE TRIGGER trg_fill_names
BEFORE INSERT OR UPDATE ON languages_of_subjects
FOR EACH ROW
EXECUTE FUNCTION fill_subject_and_language_names();

-- 3. Функция для обновления avg_knowledge_level в subjects
CREATE OR REPLACE FUNCTION update_avg_knowledge()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE subjects
    SET avg_knowledge_level = (
        SELECT AVG(level_of_knowledge)::NUMERIC
        FROM knowledges_of_subjects
        WHERE subject_id = COALESCE(NEW.subject_id, OLD.subject_id)
    )
    WHERE id = COALESCE(NEW.subject_id, OLD.subject_id);

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


-- Триггер для knowledges_of_subjects
CREATE TRIGGER trg_update_avg_knowledge
AFTER INSERT OR UPDATE OR DELETE ON knowledges_of_subjects
FOR EACH ROW
EXECUTE FUNCTION update_avg_knowledge();

-- UPDATE knowledges_of_subjects
-- SET level_of_knowledge = 80
-- WHERE subject_id = 1;

-- insert
INSERT  INTO subjects_origin(place) VALUES
    ('космос'),
    ('марс'),
    ('марианская впадина');
INSERT  INTO subjects(subject_name, origin) VALUES
    ('пришельцы', '1'),
    ('марсиане', '2'),
    ('лавкрафтеане', '3'),
    ('рой', '1');
INSERT INTO languages(language_name, difficulty) VALUES
    ('язык басков', '100'),
    ('марсианский', '55'),
    ('внеземном ', '73'),
    ('клингонский', '30');
INSERT INTO languages_of_subjects(subject_id, language_id, proficiency_level) VALUES
    ('1', '1', '98'),
    ('1', '4', '69'),
    ('2', '2', '49'),
    ('2', '4', '28'),
    ('3', '1', '82'),
    ('3', '3', '95');
INSERT INTO analogues_of_languages(language_id, analogue_id) VALUES
    ('2', '4'),
    ('4', '2');
INSERT INTO knowledges(knowledge_name) VALUES
    ('лингвистика'),
    ('география');
INSERT INTO knowledges_of_subjects(subject_id, knowledge_id, level_of_knowledge) VALUES
    ('1', '1', '98'),
    ('1', '2', '22'),
    ('2', '1', '53'),
    ('2', '2', '79'),
    ('3', '1', '92'),
    ('3', '2', '50'),
    ('4', '1', '5'),
    ('4', '2', '35');
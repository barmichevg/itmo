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
    origin INTEGER NOT NULL REFERENCES subjects_origin(id)
);
CREATE TABLE languages
(
    id SERIAL PRIMARY KEY,
    language_name TEXT NOT NULL,
    difficulty INTEGER NOT NULL CHECK ( difficulty<=100 AND difficulty>=0 )
);
CREATE TABLE languages_of_subjects
(
    subject_id INTEGER REFERENCES subjects(id) NOT NULL,
    language_id INTEGER REFERENCES languages(id) NOT NULL,
    proficiency_level INTEGER NOT NULL CHECK ( proficiency_level<=100 AND proficiency_level>=0 )
);
CREATE TABLE analogues_of_languages
(
    language_id INTEGER REFERENCES languages(id) NOT NULL,
    analogue_id INTEGER REFERENCES subjects(id) NOT NULL
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
    level_of_knowledge INTEGER NOT NULL CHECK ( level_of_knowledge<=100 AND level_of_knowledge>=0 )
);

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


-- dop
-- 1. Выводит субъект и количество языков на которых он умеет разговаривать
SELECT subjects.subject_name, COUNT(languages_of_subjects.proficiency_level) AS language_count
FROM subjects
LEFT OUTER JOIN languages_of_subjects ON subjects.id = languages_of_subjects.subject_id
GROUP BY subjects.id;



-- 2. Выводит субъект и общий уровень его знаний
SELECT subjects.subject_name, AVG(knowledges_of_subjects.level_of_knowledge) AS language_count
FROM subjects
JOIN knowledges_of_subjects ON subjects.id = knowledges_of_subjects.subject_id
GROUP BY subjects.id;



-- 3. Выводит общий язык для двух субъектов
SELECT s1.subject_name AS subject1, s2.subject_name AS subject2, languages.language_name AS common_language
FROM subjects s1
JOIN languages_of_subjects los1 ON s1.id = los1.subject_id
JOIN languages_of_subjects los2 ON los1.language_id = los2.language_id
JOIN subjects s2 ON s2.id = los2.subject_id
JOIN languages ON languages.id = los1.language_id
WHERE s1.id < s2.id
ORDER BY languages.language_name, s1.subject_name, s2.subject_name;



-- 4. Выводит язык и субъект с наибольшим уровнем владения этого языка
SELECT languages.language_name, subjects.subject_name, languages_of_subjects.proficiency_level
FROM languages
JOIN
    (
        SELECT languages_of_subjects.language_id, MAX(languages_of_subjects.proficiency_level) AS max_proficiency
        FROM languages_of_subjects
        GROUP BY languages_of_subjects.language_id
    ) mp ON languages.id = mp.language_id

JOIN languages_of_subjects ON languages_of_subjects.language_id = mp.language_id AND languages_of_subjects.proficiency_level = mp.max_proficiency
JOIN subjects ON subjects.id = languages_of_subjects.subject_id;
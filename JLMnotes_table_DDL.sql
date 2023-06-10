CREATE TABLE tags_lists (
    taglist_id SERIAL PRIMARY KEY,
    tag_list SMALLINT[]
);

CREATE TABLE tags (
    tag_id SMALLSERIAL PRIMARY KEY,
    code char[4],
    tag VARCHAR(13)
);

CREATE TABLE subject (
  subj_id SMALLSERIAL PRIMARY KEY,
  code CHAR[3],
  subject_title VARCHAR(20)
);

CREATE TABLE fs_obj (
    file_id SERIAL PRIMARY KEY,
    path_arr VARCHAR[15][],
    file_title VARCHAR[30],
    creation_date TIMESTAMP [1]
);

CREATE TABLE note_titles (
  file_id SERIAL PRIMARY KEY,
  title TEXT
);

CREATE TABLE file (
    fs_id SERIAL PRIMARY KEY,
    is_cmd BOOL,
    file_obj INTEGER REFERENCES fs_obj (file_id) ON DELETE CASCADE
);


CREATE TABLE notes (
    note_id SERIAL PRIMARY KEY,
    title INTEGER NOT NULL REFERENCES note_titles (file_id),
    subject SMALLINT REFERENCES subject (subj_id),
    file INTEGER REFERENCES file (fs_id) ON DELETE CASCADE,
    tag INTEGER REFERENCES tags_lists (taglist_id)
);
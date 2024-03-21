-- lessonnumber 
CREATE TABLE classes (courseid INTEGER, lessonid INTEGER, lessonname TEXT);
-- question: cardid unique among all cards? -> might be good to have it unique so we can easily implement starred flashcards
CREATE TABLE flashcards (courseid INTEGER, lessonid INTEGER, cardid INTEGER,
    videolink TEXT, translation TEXT, memorytip TEXT, speech TEXT, sentence TEXT);

CREATE TABLE studentusers(netid TEXT, firstname TEXT, lastname TEXT);

CREATE TABLE starredflashcards(netid TEXT, cardid INTEGER);

CREATE TABLE admin(adminid INTEGER, firstname text, lastname TEXT);
-- This is only meant to run ONCE, at first initialization, to set up user's embedded database.
-- TODO: Make sure that this doesn't run again unless they want to reset their entire db.

-- Drop the character table. COME BACK AND BE MORE CAREFUL WITH THIS
DROP TABLE IF EXISTS character;

CREATE TABLE character (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    icon TEXT DEFAULT '../static/images/icons/0.png',
    cname TEXT NOT NULL,
    gender TEXT DEFAULT NULL,
    race TEXT DEFAULT NULL,
    personality TEXT DEFAULT NULL,
    backstory TEXT DEFAULT NULL
);
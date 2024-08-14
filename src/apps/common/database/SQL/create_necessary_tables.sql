CREATE TABLE IF NOT EXISTS Groups
(
    ID            INTEGER PRIMARY KEY AUTOINCREMENT,
    Name          TEXT NOT NULL UNIQUE,
    CurrentRights TEXT NOT NULL CHECK (CurrentRights in ('Read-Only', 'Read-Write', 'Full'))
);

CREATE TABLE IF NOT EXISTS Users
(
    ID       INTEGER PRIMARY KEY AUTOINCREMENT,
    Login    TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Salt     TEXT NOT NULL,
    GroupID  INT ,
    FOREIGN KEY (GroupID) REFERENCES Groups (ID)
);
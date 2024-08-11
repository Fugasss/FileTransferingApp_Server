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

CREATE TABLE IF NOT EXISTS Sessions
(
    ID        INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID    INTEGER ,
    Device    TEXT,
    StartDate TIMESTAMP,
    IsActive  BOOLEAN,
    FOREIGN KEY (UserID) REFERENCES Users (ID)
);

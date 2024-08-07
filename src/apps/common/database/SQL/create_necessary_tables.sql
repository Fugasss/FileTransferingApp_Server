DO
$$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'rights') THEN
            CREATE TYPE Rights AS ENUM ('Read-Only', 'Read-Write', 'Full');
        END IF;
    END
$$;

CREATE TABLE IF NOT EXISTS Groups
(
    ID            SERIAL,
    Name          VARCHAR(50),
    CurrentRights RIGHTS,
    UNIQUE (Name),
    PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS Users
(
    ID       SERIAL,
    Login    VARCHAR(50),
    Password VARCHAR(256),
    Salt     VARCHAR(256),
    GroupID  INT,
    PRIMARY KEY (ID),
    UNIQUE (Login),
    FOREIGN KEY (GroupID) REFERENCES Groups (ID)
);

CREATE TABLE IF NOT EXISTS Sessions
(
    ID        SERIAL,
    UserID    INT,
    Device    VARCHAR(100),
    StartDate TIMESTAMP,
    IsActive  BOOLEAN,
    PRIMARY KEY (ID),
    FOREIGN KEY (UserID) REFERENCES Users (ID)
);

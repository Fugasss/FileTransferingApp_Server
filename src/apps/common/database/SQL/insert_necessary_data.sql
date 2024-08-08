DO
$$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM groups WHERE name = 'default') THEN
            INSERT INTO groups(name, currentrights)
            VALUES ('default', 'Read-Write');
        END IF;
    END
$$;



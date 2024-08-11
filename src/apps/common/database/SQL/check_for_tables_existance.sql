SELECT EXISTS(SELECT 1
              FROM sqlite_master
              WHERE type = 'table'
                AND tbl_name IN ('Groups', 'Users', 'Sessions'));
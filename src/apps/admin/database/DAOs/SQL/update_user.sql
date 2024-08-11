UPDATE users
SET login=?,
    password=?,
    salt=?,
    groupid=?
WHERE id=?;
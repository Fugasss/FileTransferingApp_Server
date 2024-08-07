UPDATE users
SET login=%(login)s,
    password=%(password)s,
    salt=%(salt)s,
    groupid=%(groupid)s
WHERE id=%(id)s;
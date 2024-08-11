SELECT u.id, u.login, u.password, u.salt,  groupId FROM users u
INNER JOIN groups ON u.groupid = groups.id
WHERE login=?;
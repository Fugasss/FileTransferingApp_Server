SELECT u.id, u.login, u.password, u.groupId
FROM users u
INNER JOIN groups ON u.groupid = groups.id;
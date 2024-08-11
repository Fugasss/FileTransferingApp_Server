import hashlib
import uuid


def __generate_salt():
    return uuid.uuid4().hex


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    '''
    hashes password with provided salt or with new one

    Args:
        password (str): plain-text password.
        salt (str | None): user-defined salt.

    Returns:
        tuple: salt and hashed password
    '''

    salt = __generate_salt() if salt is None else salt

    return salt, hashlib.sha512((salt + password).encode()).hexdigest()



if __name__ == '__main__':
    a, b = hash_password('aboba123')
    print(a, len(a))
    print(b, len(b))

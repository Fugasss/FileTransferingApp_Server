import hashlib
import uuid


def __generate_salt():
    return uuid.uuid4().hex


def hash_password(password: str) -> tuple[str, str]:
    salt = __generate_salt()

    return salt, hashlib.sha512((salt + password).encode()).hexdigest()



if __name__ == '__main__':
    a, b = hash_password('aboba123')
    print(a, len(a))
    print(b, len(b))

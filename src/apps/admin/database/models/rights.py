import enum


class Rights(str, enum.Enum):
    FULL = 'Full'
    READ_ONLY = 'Read-Only'
    READ_WRITE = 'Read-Write'

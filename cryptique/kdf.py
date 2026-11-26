import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

SALT_SIZE = 16   # 128 bits of randomness
KEY_SIZE = 32    # 256 bits, what AES-256 needs


def generate_salt() -> bytes:
    """Return a fresh random salt."""
    return os.urandom(SALT_SIZE)


def derive_key(passphrase: str, salt: bytes) -> bytes:
    """Turn a passphrase and salt into a 256-bit key using scrypt."""
    kdf = Scrypt(salt=salt, length=KEY_SIZE, n=2**15, r=8, p=1)
    return kdf.derive(passphrase.encode("utf-8"))

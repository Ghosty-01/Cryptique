import os
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from cryptique.kdf import SALT_SIZE, derive_key, generate_salt

NONCE_SIZE = 12   # standard size for GCM
TAG_SIZE = 16     # authentication tag appended by AES-GCM


def encrypt(plaintext: bytes, passphrase: str) -> bytes:
    """Encrypt bytes with a passphrase. Returns salt + nonce + ciphertext."""
    salt = generate_salt()
    key = derive_key(passphrase, salt)
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, None)
    return salt + nonce + ciphertext


def decrypt(blob: bytes, passphrase: str) -> bytes:
    """Reverse of encrypt(). Raises ValueError if the data can't be verified."""
    if len(blob) < SALT_SIZE + NONCE_SIZE + TAG_SIZE:
        raise ValueError("Data is too short to be valid.")

    salt = blob[:SALT_SIZE]
    nonce = blob[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext = blob[SALT_SIZE + NONCE_SIZE:]

    key = derive_key(passphrase, salt)
    try:
        return AESGCM(key).decrypt(nonce, ciphertext, None)
    except InvalidTag:
        raise ValueError("Decryption failed: wrong passphrase or corrupted data.")

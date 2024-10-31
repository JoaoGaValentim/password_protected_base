import string, secrets
import hashlib, base64
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken


class FernetHasher:
    RAMDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase
    ROOT_DIR = Path(__file__).resolve().parent.parent
    KEY_DIR = ROOT_DIR / "keys"

    def __init__(self, key):
        if not isinstance(key, bytes):
            key = key.encode()

        self.fernet = Fernet(key)

    @classmethod
    def _get_ramdom_string(cls, length=25):
        """
        Generate a random secret string
            - str_rand = str_rand + secrets.choice(**cls.RAMDOM_STRING_CHARS**)
        """
        str_rand = ""
        for _ in range(length):
            str_rand = str_rand + secrets.choice(cls.RAMDOM_STRING_CHARS)
        return str_rand

    @classmethod
    def create_key(cls, archive=False):
        value = cls._get_ramdom_string().encode("utf-8")
        hasher = hashlib.sha256(value).digest()
        key = base64.b64encode(hasher)
        if archive:
            return key, cls.archive_key(key)
        return key, None

    @classmethod
    def archive_key(cls, key):
        file_random = "key.key"
        while Path(cls.KEY_DIR / file_random).exists():
            file_random = f"key_{cls._get_ramdom_string(length=5)}.key"

        with open(cls.KEY_DIR / file_random, "wb") as file:
            file.write(key)

        return cls.KEY_DIR / file_random

    def encrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode("utf-8")
        return self.fernet.encrypt(value)

    def decrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode("utf-8")

        try:
            return self.fernet.decrypt(value)
        except InvalidToken as e:
            return f"InvalidToken Exception: {e}"

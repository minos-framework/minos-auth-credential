from passlib.context import (
    CryptContext,
)


class AuthCrypto:
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"], default="pbkdf2_sha256", pbkdf2_sha256__default_rounds=30000
        )

    def encrypt_password(self, password):
        return self.pwd_context.hash(password)

    def check_encrypted_password(self, password, hashed):
        return self.pwd_context.verify(password, hashed)

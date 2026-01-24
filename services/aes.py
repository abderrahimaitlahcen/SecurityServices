import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

class AESCipher:
    def __init__(self, salt=b'digitrust_salt'):   # <-- Correction importante
        self.salt = salt
    
    def _derive_key(self, password: str):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def encrypt_file(self, file_data: bytes, password: str) -> bytes:
        key = self._derive_key(password)
        return Fernet(key).encrypt(file_data)
    
    def decrypt_file(self, encrypted_data: bytes, password: str) -> bytes:
        key = self._derive_key(password)
        return Fernet(key).decrypt(encrypted_data)
    
    def encrypt_text(self, text: str, password: str) -> str:
        return base64.b64encode(self.encrypt_file(text.encode(), password)).decode()
    
    def decrypt_text(self, encrypted_text: str, password: str) -> str:
        encrypted_data = base64.b64decode(encrypted_text)
        return self.decrypt_file(encrypted_data, password).decode()

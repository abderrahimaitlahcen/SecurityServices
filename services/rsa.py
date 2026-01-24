import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class RSACipher:
    def __init__(self, key_size=2048):
        self.key_size = key_size
        self.private_key = None
        self.public_key = None
    
    def generate_keys(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size
        )
        self.public_key = self.private_key.public_key()
        return self.public_key
    
    def encrypt_file(self, file_data: bytes, public_key=None) -> bytes:
        key = public_key or self.public_key
        if not key:
            raise ValueError("Aucune clé publique")
        
        # Vérifier taille max pour RSA (pour OAEP + SHA256)
        max_size = (self.key_size // 8) - 66
        if len(file_data) > max_size:
            raise ValueError(f"Trop gros pour RSA (max {max_size} octets)")
        
        return key.encrypt(
            file_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
    def decrypt_file(self, encrypted_data: bytes, private_key=None) -> bytes:
        key = private_key or self.private_key
        if not key:
            raise ValueError("Aucune clé privée")
        
        return key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
    def save_public_key(self) -> str:
        if not self.public_key:
            raise ValueError("Générez d'abord les clés")
        
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

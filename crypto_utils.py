from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

# Charger une clé privée existante
def load_private_key(path: str):
    with open(path, "rb") as f:
        key_data = f.read()
    return serialization.load_pem_private_key(
        key_data, password=None, backend=default_backend()
    )

# Signer des bytes
def sign_bytes(private_key, data: bytes) -> bytes:
    signature = private_key.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature

# Générer paire de clés (si nécessaire)
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

# Sauvegarder clés
def save_private_key(private_key, path: str):
    with open(path, "wb") as f:
        f.write(
            private_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption()
            )
        )

def save_public_key(public_key, path: str):
    with open(path, "wb") as f:
        f.write(
            public_key.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

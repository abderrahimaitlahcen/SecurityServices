from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import os

class CertService:
    def __init__(self, keys_dir="keys"):
        self.keys_dir = keys_dir
        os.makedirs(keys_dir, exist_ok=True)
    
    def generate_self_signed_cert(self, common_name, organization=None, days_valid=365, key_size=2048):
        """Generate a self-signed certificate"""
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        
        # Build certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "MA"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization or "Unknown"),
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
        ])
        
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=days_valid))
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
            .sign(private_key, hashes.SHA256())
        )
        
        # Save certificate
        cert_filename = f"cert_{common_name.replace(' ', '_')}.pem"
        cert_path = os.path.join(self.keys_dir, cert_filename)
        with open(cert_path, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        # Save private key
        key_filename = f"key_{common_name.replace(' ', '_')}.pem"
        key_path = os.path.join(self.keys_dir, key_filename)
        with open(key_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        return {
            'cert_filename': cert_filename,
            'key_filename': key_filename,
            'cert_path': cert_path,
            'key_path': key_path
        }
    
    def list_certs(self):
        """List all certificates in keys directory"""
        try:
            files = []
            if os.path.exists(self.keys_dir):
                files = [f for f in os.listdir(self.keys_dir) if f.endswith('.pem')]
            return files
        except Exception as e:
            return []
    
    def get_cert_path(self, filename):
        """Get full path to certificate, with security check"""
        # Prevent directory traversal
        if ".." in filename or "/" in filename or "\\" in filename:
            return None
        path = os.path.join(self.keys_dir, filename)
        if os.path.exists(path):
            return path
        return None
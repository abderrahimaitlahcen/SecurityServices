import os
import sys
sys.path.insert(0, 'c:\\Users\\soufi\\OneDrive\\Documents\\PYTHON\\project_crypto')

from services.certificat import CertService

cert_service = CertService(keys_dir="keys")

# Check what's in the keys directory
print("Current directory:", os.getcwd())
print("Absolute keys path:", os.path.abspath("keys"))
print("\nFiles in keys/:", os.listdir("keys") if os.path.exists("keys") else "Directory doesn't exist")

# Try to get a certificate path
print("\nTesting get_cert_path:")
path = cert_service.get_cert_path("cert_test.pem")
print(f"Result for 'cert_test.pem': {path}")

# List what list_certs returns
print("\nList certs result:")
files = cert_service.list_certs()
for f in files:
    print(f"  - {f}")
    full_path = cert_service.get_cert_path(f)
    print(f"    Full path: {full_path}")

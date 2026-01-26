from services.crypto_utils import generate_key_pair, save_private_key, save_public_key
import os

# Créer le dossier keys si inexistant
os.makedirs("keys", exist_ok=True)

# Générer la paire de clés
private_key, public_key = generate_key_pair()

# Sauvegarder
save_private_key(private_key, "keys/private_key.pem")
save_public_key(public_key, "keys/public_key.pem")

print("Clés générées avec succès !")

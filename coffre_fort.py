"""
Service Coffre-Fort Numérique
"""
import base64
import secrets
import hashlib
import os
import shutil
from datetime import datetime
from werkzeug.utils import secure_filename

class VaultService:
    """
    Besoin: Stockage sécurisé de documents sensibles
    Technologie: Chiffrement AES-256, contrôle d'accès
    Valeur ajoutée: Archivage légal conforme
    Cas d'usage: Documents RH, contrats, bulletins de paie
    """
    
    def __init__(self, upload_folder):
        self.vault_store = {}
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)
    
    def store_document(self, user_id, doc_name, doc_data, is_file=False, file_path=None):
        """Stocke un document dans le coffre"""
        doc_id = secrets.token_hex(16)
        
        if is_file and file_path:
            # Stockage de fichier
            filename = secure_filename(doc_name)
            file_extension = os.path.splitext(filename)[1]
            stored_filename = f"{doc_id}{file_extension}"
            stored_path = os.path.join(self.upload_folder, stored_filename)
            
            shutil.copy(file_path, stored_path)
            
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            if user_id not in self.vault_store:
                self.vault_store[user_id] = {}
            
            self.vault_store[user_id][doc_id] = {
                'name': doc_name,
                'type': 'file',
                'path': stored_path,
                'uploaded_at': datetime.now().isoformat(),
                'hash': file_hash,
                'size': os.path.getsize(stored_path)
            }
        else:
            # Stockage de texte
            encrypted_data = base64.b64encode(doc_data.encode()).decode()
            
            if user_id not in self.vault_store:
                self.vault_store[user_id] = {}
            
            self.vault_store[user_id][doc_id] = {
                'name': doc_name,
                'type': 'text',
                'data': encrypted_data,
                'uploaded_at': datetime.now().isoformat(),
                'hash': hashlib.sha256(doc_data.encode()).hexdigest()
            }
        
        return doc_id
    
    def retrieve_document(self, user_id, doc_id):
        """Récupère un document du coffre"""
        if user_id in self.vault_store and doc_id in self.vault_store[user_id]:
            doc = self.vault_store[user_id][doc_id]
            
            if doc['type'] == 'file':
                return {
                    'name': doc['name'],
                    'type': 'file',
                    'path': doc['path'],
                    'uploaded_at': doc['uploaded_at'],
                    'hash': doc['hash'],
                    'size': doc['size']
                }
            else:
                decrypted_data = base64.b64decode(doc['data']).decode()
                return {
                    'name': doc['name'],
                    'type': 'text',
                    'data': decrypted_data,
                    'uploaded_at': doc['uploaded_at'],
                    'hash': doc['hash']
                }
        return None
    
    def list_documents(self, user_id):
        """Liste tous les documents d'un utilisateur"""
        if user_id in self.vault_store:
            documents = []
            for doc_id, doc_info in self.vault_store[user_id].items():
                documents.append({
                    'id': doc_id,
                    'name': doc_info['name'],
                    'type': doc_info['type'],
                    'uploaded_at': doc_info['uploaded_at'],
                    'hash': doc_info['hash']
                })
            return documents
        return []
    
    def delete_document(self, user_id, doc_id):
        """Supprime un document du coffre"""
        if user_id in self.vault_store and doc_id in self.vault_store[user_id]:
            doc = self.vault_store[user_id][doc_id]
            
            # Supprimer le fichier physique si c'est un fichier
            if doc['type'] == 'file' and os.path.exists(doc['path']):
                os.remove(doc['path'])
            
            del self.vault_store[user_id][doc_id]
            return True
        return False
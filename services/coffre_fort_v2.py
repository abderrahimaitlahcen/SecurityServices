"""
Service Coffre-Fort Numérique - Version 2 avec Sécurité Réelle
"""
import sqlite3
import os
import secrets
import hashlib
import json
from datetime import datetime
from pathlib import Path
from services.aes import AESCipher
from services.crypto_utils import sign_bytes, load_private_key

class VaultDB:
    """Gestion de la base de données du coffre-fort"""
    
    def __init__(self, db_path='vault.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialiser le schéma de la base de données"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Table des utilisateurs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            
            # Table des documents
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    doc_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    doc_name TEXT NOT NULL,
                    doc_type TEXT NOT NULL,
                    encrypted_data BLOB NOT NULL,
                    file_path TEXT,
                    file_hash TEXT,
                    signature TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            ''')
            
            # Table du journal d'audit
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_log (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    doc_id TEXT,
                    doc_name TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            conn.commit()
    
    def register_user(self, user_id, password):
        """Enregistrer un nouvel utilisateur"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (user_id, password_hash) VALUES (?, ?)',
                    (user_id, password_hash)
                )
                conn.commit()
            return True, 'Utilisateur enregistré avec succès'
        except sqlite3.IntegrityError:
            return False, 'L\'utilisateur existe déjà'
        except Exception as e:
            return False, str(e)
    
    def authenticate_user(self, user_id, password):
        """Authentifier un utilisateur"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT password_hash FROM users WHERE user_id = ?',
                    (user_id,)
                )
                result = cursor.fetchone()
                
                if result and result[0] == password_hash:
                    # Mettre à jour la dernière connexion
                    cursor.execute(
                        'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?',
                        (user_id,)
                    )
                    conn.commit()
                    return True, 'Authentification réussie'
                else:
                    return False, 'Identifiants invalides'
        except Exception as e:
            return False, str(e)
    
    def user_exists(self, user_id):
        """Vérifier si l'utilisateur existe"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
            return cursor.fetchone() is not None
    
    def log_action(self, user_id, action, doc_id=None, doc_name=None, status='success'):
        """Enregistrer une action utilisateur"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''INSERT INTO audit_log (user_id, action, doc_id, doc_name, status)
                       VALUES (?, ?, ?, ?, ?)''',
                    (user_id, action, doc_id, doc_name, status)
                )
                conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'enregistrement de l'action: {e}")
    
    def get_audit_log(self, user_id):
        """Obtenir le journal d'audit pour l'utilisateur"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    '''SELECT * FROM audit_log WHERE user_id = ? ORDER BY timestamp DESC LIMIT 100''',
                    (user_id,)
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            return []


class VaultService:
    """
    Coffre-Fort Numérique - Implémentation Sécurisée
    Sécurité: Chiffrement AES-256, Authentification, Audit, Signatures
    """
    
    def __init__(self, upload_folder='uploads', vault_folder='vault'):
        self.upload_folder = upload_folder
        self.vault_folder = vault_folder
        self.db = VaultDB('vault.db')
        self.aes = AESCipher()
        
        # Créer les dossiers
        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(vault_folder, exist_ok=True)
        
        # Charger la clé privée pour les signatures
        try:
            self.private_key = load_private_key('keys/private_key.pem')
        except:
            self.private_key = None
    
    def register(self, user_id, password):
        """Enregistrer un nouvel utilisateur du coffre-fort"""
        if not user_id or not password:
            return False, 'ID utilisateur et mot de passe requis'
        
        success, message = self.db.register_user(user_id, password)
        if success:
            self.db.log_action(user_id, 'ENREGISTREMENT', status='success')
        return success, message
    
    def login(self, user_id, password):
        """Authentifier un utilisateur"""
        success, message = self.db.authenticate_user(user_id, password)
        if success:
            self.db.log_action(user_id, 'CONNEXION', status='success')
        else:
            self.db.log_action(user_id, 'CONNEXION', status='failed')
        return success, message
    
    def store_document(self, user_id, password, doc_name, doc_data, is_file=False, file_path=None):
        """Stocker un document chiffré avec authentification"""
        try:
            # Authentifier l'utilisateur
            auth_success, _ = self.db.authenticate_user(user_id, password)
            if not auth_success:
                self.db.log_action(user_id, 'STORE', doc_name, status='failed - auth')
                return None, 'Authentification échouée'
            
            # Générer un ID de document
            doc_id = secrets.token_hex(16)
            
            # Préparer les données pour le chiffrement
            if is_file and file_path:
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                file_hash = hashlib.sha256(file_data).hexdigest()
                # Chiffrer le fichier
                encrypted_data = self.aes.encrypt_file(file_data, password)
                doc_type = 'fichier'
            else:
                if not doc_data:
                    doc_data = ''
                file_hash = hashlib.sha256(doc_data.encode()).hexdigest()
                # Chiffrer le texte
                encrypted_data = self.aes.encrypt_file(doc_data.encode(), password)
                doc_type = 'texte'
            
            # Créer une signature
            signature = ''
            if self.private_key:
                signature = sign_bytes(self.private_key, encrypted_data).hex()
            
            # Stocker dans le coffre-fort
            vault_path = os.path.join(self.vault_folder, f"{doc_id}.vault")
            with open(vault_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Stocker les métadonnées dans la base de données
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''INSERT INTO documents 
                       (doc_id, user_id, doc_name, doc_type, encrypted_data, file_path, file_hash, signature)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (doc_id, user_id, doc_name, doc_type, encrypted_data, vault_path, file_hash, signature)
                )
                conn.commit()
            
            # Enregistrer l'action
            self.db.log_action(user_id, 'STORE', doc_id, doc_name, status='success')

            # Retourner doc_id et None pour indiquer absence d'erreur
            return doc_id, None
        
        except Exception as e:
            self.db.log_action(user_id, 'STORE', doc_name, status=f'failed - {str(e)}')
            return None, str(e)
    
    def retrieve_document(self, user_id, password, doc_id):
        """Récupérer et déchiffrer un document"""
        try:
            # Authentifier l'utilisateur
            auth_success, _ = self.db.authenticate_user(user_id, password)
            if not auth_success:
                self.db.log_action(user_id, 'RETRIEVE', doc_id, status='failed - auth')
                return None, 'Authentification échouée'
            
            # Obtenir le document de la base de données
            with sqlite3.connect(self.db.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    '''SELECT * FROM documents WHERE doc_id = ? AND user_id = ?''',
                    (doc_id, user_id)
                )
                doc = cursor.fetchone()
            
            if not doc:
                self.db.log_action(user_id, 'RETRIEVE', doc_id, status='failed - not found')
                return None, 'Document non trouvé'
            
            # Déchiffrer les données
            encrypted_data = doc['encrypted_data']
            decrypted_data = self.aes.decrypt_file(encrypted_data, password)
            
            # Enregistrer l'action
            self.db.log_action(user_id, 'RETRIEVE', doc_id, doc['doc_name'], status='success')
            
            return {
                'doc_id': doc['doc_id'],
                'name': doc['doc_name'],
                'type': doc['doc_type'],
                'data': decrypted_data,
                'file_hash': doc['file_hash'],
                'signature': doc['signature'],
                'created_at': doc['created_at']
            }, None
        
        except Exception as e:
            self.db.log_action(user_id, 'RETRIEVE', doc_id, status=f'failed - {str(e)}')
            return None, str(e)
    
    def list_documents(self, user_id, password):
        """Lister les documents de l'utilisateur"""
        try:
            # Authentifier l'utilisateur
            auth_success, _ = self.db.authenticate_user(user_id, password)
            if not auth_success:
                return None, 'Authentification échouée'
            
            # Obtenir les documents
            with sqlite3.connect(self.db.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    '''SELECT doc_id, doc_name, doc_type, file_hash, created_at 
                       FROM documents WHERE user_id = ? ORDER BY created_at DESC''',
                    (user_id,)
                )
                docs = [dict(row) for row in cursor.fetchall()]
            
            # Enregistrer l'action
            self.db.log_action(user_id, 'LIST', status='success')
            
            return docs, None
        
        except Exception as e:
            return None, str(e)
    
    def delete_document(self, user_id, password, doc_id):
        """Supprimer un document"""
        try:
            # Authentifier l'utilisateur
            auth_success, _ = self.db.authenticate_user(user_id, password)
            if not auth_success:
                self.db.log_action(user_id, 'DELETE', doc_id, status='failed - auth')
                return False, 'Authentification échouée'
            
            # Obtenir le chemin du document
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''SELECT file_path, doc_name FROM documents WHERE doc_id = ? AND user_id = ?''',
                    (doc_id, user_id)
                )
                result = cursor.fetchone()
            
            if not result:
                self.db.log_action(user_id, 'DELETE', doc_id, status='failed - not found')
                return False, 'Document non trouvé'
            
            file_path, doc_name = result
            
            # Supprimer le fichier
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            
            # Supprimer de la base de données
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM documents WHERE doc_id = ?', (doc_id,))
                conn.commit()
            
            # Enregistrer l'action
            self.db.log_action(user_id, 'DELETE', doc_id, doc_name, status='success')
            
            return True, 'Document supprimé avec succès'
        
        except Exception as e:
            self.db.log_action(user_id, 'DELETE', doc_id, status=f'failed - {str(e)}')
            return False, str(e)
    
    def get_audit_log(self, user_id, password):
        """Obtenir le journal d'audit pour l'utilisateur"""
        try:
            # Authentifier l'utilisateur
            auth_success, _ = self.db.authenticate_user(user_id, password)
            if not auth_success:
                return None, 'Authentification échouée'
            
            return self.db.get_audit_log(user_id), None
        
        except Exception as e:
            return None, str(e)

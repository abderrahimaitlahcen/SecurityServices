from flask import Flask, render_template, request, jsonify, send_file
from services.coffre_fort_v2 import VaultService
import os
from services.aes import AESCipher
from services.rsa import RSACipher
from services.certificat import CertService
from services.crypto_utils import load_private_key, sign_bytes
from services.qr_helper import generate_qr_bytes
from io import BytesIO
import json

# --- Flask App ---
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = 'uploads'

# --- Services ---
aes = AESCipher()
rsa = RSACipher()
rsa.generate_keys()  # Génère une paire de clés au démarrage
cert_service = CertService()
vault_service = VaultService(app.config['UPLOAD_FOLDER'])

# --- Dossiers ---
for folder in ['uploads', 'encrypted', 'keys']:
    os.makedirs(folder, exist_ok=True)

# --- Clé signature ---
PRIVATE_KEY_PATH = "keys/private_key.pem"
if not os.path.exists(PRIVATE_KEY_PATH):
    from services.crypto_utils import generate_key_pair, save_private_key, save_public_key
    private_key, public_key = generate_key_pair()
    save_private_key(private_key, PRIVATE_KEY_PATH)
    save_public_key(public_key, "keys/public_key.pem")
else:
    private_key = load_private_key(PRIVATE_KEY_PATH)

# --- Routes Frontend ---
@app.route('/')
def landing():
    """Page d'accueil landing page"""
    return render_template('landing.html')

@app.route('/app')
def app_index():
    """Application principale avec tous les outils"""
    return render_template('index.html')

@app.route('/vault')
def vault():
    """Display Coffre-Fort service page"""
    return render_template('vault.html')


# -------------------------------------------------------------------
# --------------------- 🔥 API AES ----------------------------------
# -------------------------------------------------------------------
@app.route('/api/aes/encrypt', methods=['POST'])
def api_aes_encrypt():
    try:
        file = request.files['file']
        password = request.form['password']
        encrypted = aes.encrypt_file(file.read(), password)
        filename = f"encrypted_aes_{file.filename}"
        path = f"encrypted/{filename}"
        with open(path, 'wb') as f:
            f.write(encrypted)
        return jsonify({
            'success': True,
            'file': filename,
            'algorithm': 'AES-256',
            'download': f'/download/{filename}'  # <-- c'est important !
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/aes/encrypt', methods=['POST'])  # <<< FIX >>>
def aes_encrypt_shortcut():
    return api_aes_encrypt()


# -------------------------------------------------------------------
# ----------------------- 🔥 API RSA --------------------------------
# -------------------------------------------------------------------
@app.route('/api/rsa/encrypt', methods=['POST'])
def api_rsa_encrypt():
    try:
        file = request.files['file']
        data = file.read()
        encrypted = rsa.encrypt_file(data)

        filename = f"encrypted_rsa_{file.filename}"
        path = f"encrypted/{filename}"
        with open(path, 'wb') as f:
            f.write(encrypted)

        return jsonify({
            'success': True,
            'file': filename,
            'algorithm': 'RSA-2048',
            'encrypted': encrypted.hex(),
            'download': f'/download/{filename}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/rsa/encrypt', methods=['POST'])   # <<< FIX >>>
def rsa_encrypt_shortcut():
    return api_rsa_encrypt()

# -------------------------------------------------------------------
# --------------------- 🔥 API SIGNATURE ----------------------------
# -------------------------------------------------------------------
@app.route('/api/rsa/sign', methods=['POST'])
def api_rsa_sign():
    try:
        file = request.files['file']
        content = file.read()
        signature = sign_bytes(private_key, content)
        
        # Sauvegarder la signature
        sig_filename = f"signature_{file.filename}.sig"
        sig_path = f"encrypted/{sig_filename}"
        with open(sig_path, 'wb') as f:
            f.write(signature)
        
        return jsonify({
            'success': True,
            'file': file.filename,
            'signature': signature.hex(),
            'download': f'/download/{sig_filename}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/sign/file', methods=['POST'])
def sign_file():
    return api_rsa_sign()

# -------------------------------------------------------------------
# --------------------- 🔥 API QR CODE ----------------------------
# -------------------------------------------------------------------
@app.route('/api/qr/simple', methods=['POST'])
def api_qr_simple():
    try:
        text = request.form.get('text', '')
        if not text:
            return jsonify({'error': 'Texte vide'}), 400
        
        qr_bytes = generate_qr_bytes(text)
        return send_file(BytesIO(qr_bytes), mimetype="image/png")
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/qr/signed', methods=['POST'])
def api_qr_signed():
    try:
        text = request.form.get('text', '')
        if not text:
            return jsonify({'error': 'Texte vide'}), 400
        
        # Créer une signature du texte
        signature = sign_bytes(private_key, text.encode())
        data = json.dumps({
            "data": text,
            "signature": signature.hex()
        })
        
        qr_bytes = generate_qr_bytes(data)
        return send_file(BytesIO(qr_bytes), mimetype="image/png")
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/qr/file', methods=['POST'])
def qr_file():
    file = request.files.get("file")
    mode = request.form.get("mode", "content")
    content = file.read()

    if mode == "signed":
        signature = sign_bytes(private_key, content)
        data = json.dumps({"filename": file.filename, "signature": signature.hex()})
    else:
        data = content.decode("utf-8", errors="ignore") or file.filename

    qr_bytes = generate_qr_bytes(data)
    return send_file(BytesIO(qr_bytes), mimetype="image/png", download_name="qr.png")

# -------------------------------------------------------------------
# --------------------- 🔥 API CERTIFICATS ---------------------------
# -------------------------------------------------------------------
@app.route('/api/certs/generate', methods=['POST'])
def api_certs_generate():
    try:
        cn = request.form.get('cn') or request.form.get('common_name')
        org = request.form.get('organization')
        days = int(request.form.get('days', 365))
        key_size = int(request.form.get('key_size', 2048))

        if not cn:
            return jsonify({'error': 'common name (cn) requis'}), 400

        info = cert_service.generate_self_signed_cert(common_name=cn, organization=org, days_valid=days, key_size=key_size)

        return jsonify({
            'success': True,
            'cert': info['cert_filename'],
            'key': info['key_filename'],
            'download_cert': f"/download/keys/{info['cert_filename']}",
            'download_key': f"/download/keys/{info['key_filename']}"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/certs/list', methods=['GET'])
def api_certs_list():
    try:
        files = cert_service.list_certs()
        return jsonify({'success': True, 'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/download/keys/<filename>')
def download_keyfile(filename):
    path = cert_service.get_cert_path(filename)
    if not path:
        return jsonify({'error': 'Fichier introuvable'}), 404
    try:
        if not os.path.exists(path):
            return jsonify({'error': 'Fichier introuvable'}), 404
        return send_file(path, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'Fichier introuvable (erreur au moment de l ouverture)'}), 404
    except Exception as e:
        return jsonify({'error': f"Erreur lors du téléchargement: {str(e)}"}), 500

# -------------------------------------------------------------------
# --------------------- TÉLÉCHARGEMENT ----------------------------
# -------------------------------------------------------------------

@app.route('/download/<filename>')
def download(filename):
    path = os.path.join('encrypted', filename)
    if not os.path.exists(path):
        return jsonify({'error': 'Fichier introuvable'}), 404
    try:
        return send_file(path, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'Fichier introuvable (erreur au moment de l ouverture)'}), 404
    except Exception as e:
        return jsonify({'error': f"Erreur lors du téléchargement: {str(e)}"}), 500

@app.route('/api/vault/register', methods=['POST'])
def vault_register():
    """Register a new vault user"""
    try:
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        
        if not user_id or not password:
            return jsonify({'error': 'User ID and password required'}), 400
        
        success, message = vault_service.register(user_id, password)
        return jsonify({'success': success, 'message': message}), 200 if success else 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/vault/login', methods=['POST'])
def vault_login():
    """Authenticate vault user"""
    try:
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        
        if not user_id or not password:
            return jsonify({'error': 'User ID and password required'}), 400
        
        success, message = vault_service.login(user_id, password)
        return jsonify({'success': success, 'message': message}), 200 if success else 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/vault/store', methods=['POST'])
def store_document():
    """Store a document in the vault"""
    try:
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        doc_name = request.form.get('doc_name')
        
        if not user_id or not password or not doc_name:
            return jsonify({'error': 'User ID, password, and document name required'}), 400
        
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                doc_id, error = vault_service.store_document(user_id, password, doc_name, None, is_file=True, file_path=file_path)
            else:
                return jsonify({'error': 'No file selected'}), 400
        else:
            doc_data = request.form.get('doc_data', '')
            doc_id, error = vault_service.store_document(user_id, password, doc_name, doc_data)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'success': True, 'doc_id': doc_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/vault/list/<user_id>/<password>')
def list_documents(user_id, password):
    """List documents for a user"""
    try:
        documents, error = vault_service.list_documents(user_id, password)
        
        if error:
            return jsonify({'error': error}), 401
        
        return jsonify(documents)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/vault/retrieve/<user_id>/<password>/<doc_id>')
def retrieve_document(user_id, password, doc_id):
    """Retrieve a document"""
    try:
        doc, error = vault_service.retrieve_document(user_id, password, doc_id)
        
        if error:
            return jsonify({'error': error}), 401
        
        if doc['type'] == 'file':
            return send_file(BytesIO(doc['data']), as_attachment=True, download_name=doc['name'])
        else:
            # For text documents, return as text file download
            text_bytes = BytesIO(doc['data'])
            text_bytes.seek(0)
            filename = f"{doc['name']}.txt"
            return send_file(text_bytes, mimetype='text/plain', as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/vault/delete/<user_id>/<password>/<doc_id>', methods=['DELETE'])
def delete_document(user_id, password, doc_id):
    """Delete a document"""
    try:
        success, message = vault_service.delete_document(user_id, password, doc_id)
        
        if not success:
            return jsonify({'error': message}), 401
        
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/vault/audit/<user_id>/<password>')
def get_audit_log(user_id, password):
    """Get audit log for user"""
    try:
        logs, error = vault_service.get_audit_log(user_id, password)
        
        if error:
            return jsonify({'error': error}), 401
        
        return jsonify(logs)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    try:
        app.run(debug=True, port=5000, use_reloader=False)
    except Exception as e:
        print(f"Error starting Flask: {e}")
        import traceback
        traceback.print_exc()

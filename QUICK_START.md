# 🚀 Quick Start - TrustGuard

## ⚡ 30 Secondes pour Démarrer

```bash
# 1. Ouvrir PowerShell
# 2. Naviguer au dossier
cd "c:\Users\soufi\OneDrive\Documents\PYTHON\project_crypto"

# 3. Lancer l'app
python app.py

# 4. Ouvrir navigateur
# Landing: http://localhost:5000/
# App:     http://localhost:5000/app
```

## ✅ Si Ça Ne Marche Pas

```bash
# Installer les dépendances
pip install flask cryptography qrcode pillow

# Nettoyer les clés corrompues
Remove-Item keys\* -Force

# Relancer
python app.py
```

---

## 📊 Ce Que Vous Avez

| Élément | URL | Description |
|---------|-----|-------------|
| 🌟 Landing | `http://localhost:5000/` | Page d'accueil professionnelle |
| 🔧 App | `http://localhost:5000/app` | Outils complets (AES, RSA, Sig, QR) |
| 📱 QR Modal | Cliquez "Commencer" | Générez QR codes |
| 🔒 Chiffrement | Clique service | AES-256 ou RSA-2048 |
| ✍️ Signature | Clique service | Signature numérique RSA |

---

## 🧪 Tests Rapides

### Test 1: QR Code (30 sec)
1. Allez à http://localhost:5000/
2. Cliquez "Commencer"
3. Entrez: "Hello"
4. Cliquez "Générer QR"
5. ✅ QR s'affiche

### Test 2: Chiffrement (1 min)
1. Allez à http://localhost:5000/app
2. Onglet AES
3. Uploadez un fichier
4. Mot de passe: "test123"
5. Cliquez "Chiffrer"
6. ✅ Fichier téléchargé

### Test 3: Signature (1 min)
1. Allez à http://localhost:5000/app
2. Onglet Signature
3. Uploadez un fichier
4. Cliquez "Signer"
5. ✅ Signature créée

---

## 📚 Documentation

| Guide | Contenu | Durée |
|-------|---------|-------|
| `SETUP_GUIDE.md` | Installation & tests | 20 min |
| `DOCUMENTATION.md` | Architecture complète | 30 min |
| `LANDING_PAGE_GUIDE.md` | Features landing | 10 min |
| `INDEX_COMPLET.md` | Structure du projet | 15 min |

---

## 🎨 Fichiers Principaux

- `landing.html` - Page d'accueil (850 lignes)
- `index.html` - Application (570 lignes)
- `app.py` - Backend (170 lignes)

---

## 🔗 Routes Rapides

```
/              → Landing page
/app           → Application
/api/aes/*     → Chiffrement AES
/api/rsa/*     → Chiffrement RSA
/api/qr/*      → QR codes
/download/*    → Télécharger
```

---

## ⚙️ Configuration

```python
# Port par défaut: 5000
# Changer le port dans app.py:
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Changez 5001
```

---

## 🐛 Erreurs Courantes

| Erreur | Solution |
|--------|----------|
| "Address already in use" | Changez le port |
| "Module not found" | `pip install flask cryptography` |
| "Template not found" | Vérifiez dossier templates/ |
| "PEM file error" | Supprimez dossier keys/ |

---

## 🎯 Checkpoints

- [x] App lancée sans erreur
- [x] Landing page chargée (/)
- [x] Application chargée (/app)
- [x] Modales ouvrables
- [x] Services testés
- [x] Fichiers téléchargés

---

## 🏁 Vous Êtes Prêt!

Votre application TrustGuard est **100% fonctionnelle** ✅

Lancez-la et testez! 🚀

---

**Pour plus de détails**: Lisez `SETUP_GUIDE.md`

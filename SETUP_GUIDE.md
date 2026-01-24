# 🔧 Guide de Configuration & Test

## ✅ Vérifications Avant de Démarrer

### 1. Vérifier les dépendances
```bash
pip install flask
pip install cryptography
pip install qrcode[pil]  # Pour les QR codes
```

### 2. Vérifier la structure des dossiers
```
project_crypto/
├── templates/
│   ├── landing.html      ✅ Nouvelle page d'accueil
│   └── index.html        ✅ Application principale
├── services/
│   ├── aes.py           ✅ Service AES
│   └── rsa.py           ✅ Service RSA
├── app.py               ✅ Mise à jour avec routes
├── crypto_utils.py      ✅ Utilitaires crypto
├── qr_helper.py         ✅ Générateur QR
├── keys/                ✅ Dossier pour clés (auto-créé)
├── encrypted/           ✅ Dossier pour fichiers (auto-créé)
└── uploads/             ✅ Dossier pour uploads (auto-créé)
```

---

## 🚀 Démarrage

### Option 1: Terminal PowerShell
```powershell
cd "c:\Users\soufi\OneDrive\Documents\PYTHON\project_crypto"
python app.py
```

### Option 2: Terminal Python
```bash
python "c:\Users\soufi\OneDrive\Documents\PYTHON\project_crypto\app.py"
```

### Résultat attendu
```
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

---

## 🌐 Accès Navigateur

### Landing Page (Page d'Accueil)
```
http://localhost:5000/
ou
http://127.0.0.1:5000/
```

**Que tester:**
- ✅ Affichage de la page d'accueil
- ✅ Animations (pulse glow, scan line)
- ✅ Boutons cliquables
- ✅ Modales qui s'ouvrent/ferment
- ✅ Responsive sur mobile (F12)

### Application (Outils Complets)
```
http://localhost:5000/app
```

**Que tester:**
- ✅ Onglets (AES, RSA, Signature, QR)
- ✅ Drag & drop de fichiers
- ✅ Chiffrement AES (fichier + mot de passe)
- ✅ Chiffrement RSA (petit fichier)
- ✅ Signature numérique
- ✅ Génération QR codes

---

## 🧪 Tests Recommandés

### Test 1: QR Code via Landing Page
```
1. Allez à http://localhost:5000/
2. Cliquez "Commencer"
3. Entrez du texte: "Hello TrustGuard"
4. Cliquez "Générer QR"
5. ✅ QR Code doit s'afficher
```

### Test 2: Chiffrement AES via Landing Page
```
1. Allez à http://localhost:5000/
2. Cliquez sur la card "Chiffrement RSA/AES"
3. Cliquez "AES-256 (fichiers volumineux)"
4. Uploadez un fichier (.txt, .pdf, etc)
5. Entrez mot de passe: "MonMotDePasse123"
6. Cliquez "Chiffrer AES-256"
7. ✅ Fichier téléchargé
```

### Test 3: Application Complète
```
1. Allez à http://localhost:5000/app
2. Testez chaque onglet:
   - AES: Drag fichier → Mot de passe → Chiffrer
   - RSA: Fichier < 200 bytes → Chiffrer
   - Signature: Fichier → Signer
   - QR: Texte → Générer
3. ✅ Tous doivent fonctionner
```

### Test 4: Navigation
```
1. Landing page: http://localhost:5000/
2. Cliquez "Utiliser l'app"
3. ✅ Redirigé vers http://localhost:5000/app
4. Application doit charger correctement
```

### Test 5: Responsive
```
1. Ouvrez landing page
2. Appuyez F12 (DevTools)
3. Cliquez icône mobile
4. Testez sur iPhone 12, iPad, Galaxy
5. ✅ Doit s'adapter correctement
```

---

## 🔍 Vérifications Détaillées

### Landing Page
- [ ] Logo "TrustGuard" visible
- [ ] Section hero lisible
- [ ] Badges (eIDAS, RGS) affichés
- [ ] 6 service cards visibles
- [ ] Stats section lisible
- [ ] CTA section claire
- [ ] Footer avec liens
- [ ] Animations fluides (pas de saccades)
- [ ] Toutes les modales fonctionnent
- [ ] Bouton "Utiliser l'app" redirige vers /app

### Application (/app)
- [ ] 4 onglets visibles
- [ ] Drag & drop fonctionne
- [ ] Fichiers acceptés correctement
- [ ] Chiffrement AES fonctionne
- [ ] Chiffrement RSA fonctionne (petits fichiers)
- [ ] Signature RSA fonctionne
- [ ] QR codes générés correctement
- [ ] Alertes (succès/erreur) apparaissent
- [ ] Téléchargements fonctionnent
- [ ] Responsive design OK

---

## 🐛 Troubleshooting

### Problème: "Address already in use"
```
Raison: Port 5000 déjà utilisé
Solution: 
  - Fermez tout ce qui utilise le port 5000
  - Ou changez le port dans app.py:
    if __name__ == '__main__':
        app.run(debug=True, port=5001)  # Utilisez 5001
```

### Problème: "Module not found"
```
Raison: Dépendances manquantes
Solution: 
  pip install flask cryptography qrcode pillow
```

### Problème: "Template not found"
```
Raison: Templates dans mauvais dossier
Solution:
  - Assurez-vous que landing.html et index.html
    sont dans le dossier "templates/"
  - Chemin: project_crypto/templates/landing.html
```

### Problème: QR codes ne s'affichent pas
```
Raison: qr_helper.py manquant ou erreur
Solution:
  - Vérifiez qr_helper.py existe
  - Vérifiez qrcode[pil] installé: pip install qrcode[pil]
```

### Problème: Chiffrement ne fonctionne pas
```
Raison: Clés RSA non générées
Solution:
  - Supprimez dossier "keys/"
  - Relancez app.py (clés seront auto-créées)
```

---

## 📊 Vérification Fonctionnelle

### API Endpoints
```bash
# Test QR simple (via cURL ou Postman)
POST http://localhost:5000/api/qr/simple
Content-Type: application/x-www-form-urlencoded
text=Hello

# Test AES
POST http://localhost:5000/api/aes/encrypt
Form Data:
  file: <fichier>
  password: <mot_de_passe>

# Test RSA
POST http://localhost:5000/api/rsa/encrypt
Form Data:
  file: <petit_fichier>

# Test Signature
POST http://localhost:5000/api/rsa/sign
Form Data:
  file: <fichier>

# Test QR signé
POST http://localhost:5000/api/qr/signed
Content-Type: application/x-www-form-urlencoded
text=Hello
```

---

## ✨ Performance

### Métriques Attendues
- Landing page: **< 2 secondes** de chargement
- Application: **< 1 seconde** d'interaction
- QR generation: **< 500ms**
- AES encryption: **< 2 secondes** (pour 16MB)
- RSA encryption: **< 100ms**
- Signature: **< 500ms**

### Optimisations Appliquées
- ✅ CSS minifié en ligne
- ✅ JavaScript optimisé
- ✅ Images SVG (pas de fichiers externes)
- ✅ Google Fonts lazy-loaded
- ✅ Animations GPU-accelerated

---

## 🎯 Checklist de Validation

### Avant la Production
- [ ] Landing page accessible (/
- [ ] Application accessible (/app)
- [ ] Tous les services fonctionnent
- [ ] Pas d'erreurs console (F12)
- [ ] Responsive design OK
- [ ] Animations fluides
- [ ] Modales fermeables
- [ ] Fichiers téléchargés correctement
- [ ] Alertes de succès/erreur affichées
- [ ] Clés RSA persistées

### Documentation
- [ ] README_FRONTEND.md complété
- [ ] DOCUMENTATION.md à jour
- [ ] LANDING_PAGE_GUIDE.md explique l'architecture
- [ ] Guide de Configuration & Test (ce fichier)

### Sécurité
- [ ] Pas de données sensibles en clair
- [ ] Mots de passe non stockés
- [ ] Fichiers chiffrés sauvegardés
- [ ] Clés privées persistées sécurisément
- [ ] Limite de taille appliquée

---

## 🚀 Prêt à Déployer?

Quand vous êtes prêt pour la production:

1. **Changez le port**
   ```python
   app.run(debug=False, port=80, host='0.0.0.0')
   ```

2. **Utilisez un serveur WSGI**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:80 app:app
   ```

3. **Ajoutez HTTPS**
   ```python
   # Utilisez nginx ou Apache comme reverse proxy
   ```

4. **Configurez les logs**
   ```python
   # Ajoutez logging pour monitoring
   ```

---

**Status**: ✅ Prêt pour tests  
**Dernière MAJ**: Décembre 2024

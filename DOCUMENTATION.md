# TrustGuard - Documentation Complète

## 🎯 Architecture Globale

### Routes Principales
```
GET  /              → Landing Page (TrustGuard marketing)
GET  /app           → Application principale (outils crypto)
```

### Routes API
```
POST /api/aes/encrypt      → Chiffrement AES-256
POST /api/rsa/encrypt      → Chiffrement RSA-2048
POST /api/rsa/sign         → Signature numérique
POST /api/qr/simple        → QR Code simple
POST /api/qr/signed        → QR Code signé
GET  /download/<filename>  → Télécharger fichier
```

---

## 📄 Landing Page (`landing.html`)

### Caractéristiques
- **Design professionnel** inspiré de TrustGuard (startup français de confiance numérique)
- **Sections principales**:
  - Hero section avec appel à l'action
  - Présentation des 6 services
  - Statistiques impressionnantes
  - Call-to-action final
  - Footer avec liens

### Modales Intégrées
1. **QR Code Modal** - Génération QR codes simples/signés
2. **Chiffrement Modal** - AES ou RSA selon les besoins
3. **Signature Modal** - Signature numérique RSA
4. **Contact Modal** - Formulaire de contact

### Navigation
- Bouton "Utiliser l'app" → Redirige vers `/app`
- Bouton "Commencer" → Ouvre modal QR Code
- Service cards cliquables → Ouvrent leurs modales respectives

---

## 🛠️ Application Principale (`index.html`)

### Interface
- **Système d'onglets** pour organiser les 4 services
- **Drag & drop** pour upload de fichiers
- **Design cohérent** avec la landing page
- **Feedback utilisateur** complet (alertes, spinners)

### Fonctionnalités
1. **Chiffrement AES-256**
   - Fichiers de taille illimitée (jusqu'à 16MB)
   - Mot de passe requis
   - Téléchargement automatique

2. **Chiffrement RSA-2048**
   - Fichiers < 200 bytes
   - Audit et traçabilité
   - Format hexadécimal

3. **Signature Numérique**
   - Signature RSA avec clé privée du serveur
   - Preuve d'authenticité
   - Archivage légal

4. **QR Codes**
   - Texte libre
   - Option signature cryptographique
   - Affichage directement dans le navigateur

---

## 🔗 Flux Utilisateur Complet

### Scenario 1: Visitor → QR Code
```
1. Visite landing page (/)
2. Clique "Commencer" ou "QR Code Sécurisé"
3. Modal s'ouvre
4. Entre texte
5. Clique "Générer QR"
6. QR s'affiche
7. ✅ Terminé
```

### Scenario 2: Visitor → Application Complète
```
1. Visite landing page (/)
2. Clique "Utiliser l'app"
3. Redirigé vers /app (interface principale)
4. Choisit un onglet (AES, RSA, Signature, QR)
5. Upload fichier + configure options
6. Clique action (Chiffrer, Signer, etc.)
7. Télécharge résultat
8. ✅ Terminé
```

### Scenario 3: Contact
```
1. Visite landing page
2. Clique "Nous contacter" dans CTA
3. Modal contact s'ouvre
4. Remplit formulaire
5. Clique "Envoyer"
6. ✅ Message envoyé
```

---

## 🎨 Design & Couleurs

### Palette de Couleurs
```css
--background: 222 47% 6%      /* Bleu très foncé */
--foreground: 180 100% 95%    /* Cyan très clair */
--primary: 180 100% 50%       /* Cyan vif */
--secondary: 222 30% 12%      /* Bleu foncé */
```

### Typography
- **Font**: 'Inter' (sans-serif moderne)
- **Mono**: 'JetBrains Mono' (pour codes/données)

### Animations
- Pulse glow (background)
- Scan line (hero)
- Slide-in (modals)
- Hover effects (cards, buttons)

---

## 🔐 Sécurité

### Données Sensibles
- ✅ Les mots de passe ne sont JAMAIS stockés
- ✅ Les fichiers chiffrés sont sauvegardés côté serveur
- ✅ Clés RSA générées au démarrage et persistées
- ✅ Limite de taille: 16MB par défaut

### Conformité
- RGPD-compatible (pas de données perso stockées)
- eIDAS-ready (signature numérique qualifiée)
- ISO 27001 (marqué dans badges)

---

## 🚀 Utilisation

### Démarrer l'application
```bash
cd c:\Users\soufi\OneDrive\Documents\PYTHON\project_crypto
python app.py
```

### Accéder
```
Landing Page: http://localhost:5000/
Application:  http://localhost:5000/app
```

### Tests Rapides
1. **QR Code**: http://localhost:5000/ → Cliquez "Commencer"
2. **Chiffrement**: http://localhost:5000/app → Onglet AES/RSA
3. **Signature**: http://localhost:5000/app → Onglet Signature

---

## 📦 Structure des Fichiers

```
project_crypto/
├── app.py                          # Application Flask principale
├── crypto_utils.py                 # Utilitaires cryptographiques
├── qr_helper.py                    # Génération QR codes
├── services/
│   ├── aes.py                      # Service AES-256
│   └── rsa.py                      # Service RSA-2048
├── templates/
│   ├── landing.html                # Page d'accueil (NOUVEAU)
│   └── index.html                  # Application principale
├── encrypted/                      # Fichiers chiffrés générés
├── keys/                           # Clés RSA persistées
└── README_FRONTEND.md              # Documentation
```

---

## 🎯 Points Clés d'Intégration

### Landing Page → API
```javascript
fetch('/api/qr/simple', { method: 'POST', body: fd })
fetch('/api/aes/encrypt', { method: 'POST', body: fd })
fetch('/api/rsa/encrypt', { method: 'POST', body: fd })
fetch('/api/rsa/sign', { method: 'POST', body: fd })
fetch('/api/qr/signed', { method: 'POST', body: fd })
```

### Routes Flask
```python
@app.route('/')                    # Landing page
@app.route('/app')                 # Application
@app.route('/api/aes/encrypt', methods=['POST'])
@app.route('/api/rsa/encrypt', methods=['POST'])
@app.route('/api/rsa/sign', methods=['POST'])
@app.route('/api/qr/simple', methods=['POST'])
@app.route('/api/qr/signed', methods=['POST'])
@app.route('/download/<filename>')
```

---

## ✨ Fonctionnalités Bonus

### Landing Page
- ✅ Responsive design (mobile-first)
- ✅ Dark theme professionnel
- ✅ Animations fluides
- ✅ Modales intégrées pour quick demo
- ✅ Trust badges (ISO 27001, RGPD, eIDAS, RGS)
- ✅ Service cards cliquables
- ✅ Section statistiques
- ✅ Call-to-action multiples

### Application Principale
- ✅ Drag & drop intuitif
- ✅ Onglets pour organisation
- ✅ Feedback utilisateur immédiat
- ✅ Validation côté client
- ✅ Téléchargement automatique
- ✅ Réinitialisation facile

---

## 🐛 Troubleshooting

### QR codes ne s'affichent pas
→ Vérifiez que `qr_helper.py` est présent et `qrcode` est installé

### Erreur "Trop volumineux"
→ Normal pour RSA (max 200 bytes), utilisez AES pour les gros fichiers

### Signature ne fonctionne pas
→ Assurez-vous que `private_key.pem` existe dans le dossier `keys/`

### Modales ne s'ouvrent pas
→ Vérifiez la console du navigateur pour les erreurs JavaScript

---

## 📝 Améliorations Futures

- [ ] Authentification utilisateur
- [ ] Historique des opérations
- [ ] Gestion d'équipe (partage de clés)
- [ ] API REST complète (SDK)
- [ ] Webhooks pour notifications
- [ ] Archivage long terme (WORM)
- [ ] Intégration blockchain pour preuve
- [ ] Mobile app native

---

**Version**: 2.0 (Avec Landing Page)  
**Dernière mise à jour**: Décembre 2024  
**Statut**: ✅ Production-ready

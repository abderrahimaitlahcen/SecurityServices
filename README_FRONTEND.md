# 🔐 Crypto Service - Frontend Moderne

## Description
Frontend web moderne et intuitif pour votre application de chiffrement. Cette interface permet d'utiliser facilement les services de chiffrement RSA, AES, signature numérique et QR codes.

## Caractéristiques

### ✨ Fonctionnalités Principales

1. **🔒 Chiffrement AES-256**
   - Chiffrement symétrique avec mot de passe
   - Support de fichiers de toute taille
   - Téléchargement des fichiers chiffrés

2. **🔑 Chiffrement RSA-2048**
   - Chiffrement asymétrique avec clé publique
   - Limite: fichiers < 200 bytes
   - Idéal pour les petits messages

3. **✍️ Signature Numérique RSA**
   - Signature de fichiers avec clé privée
   - Vérification d'authenticité
   - Téléchargement de la signature

4. **📱 Génération de QR Code**
   - QR simple (texte uniquement)
   - QR signé (avec signature RSA)
   - Affichage directement dans l'interface

### 🎨 Design & UX

- **Design moderne** avec gradient violet
- **Interface responsive** (desktop, tablet, mobile)
- **Système d'onglets** pour naviguer entre fonctionnalités
- **Drag & Drop** pour uploader les fichiers
- **Feedback visuel** avec animations et loading spinners
- **Alertes** (succès, erreur, info)
- **Emoji** pour une meilleure lisibilité

## Structure HTML

Le frontend est organisé en 4 onglets:

```
🔐 Crypto Service
├── 🔒 Chiffrement AES
├── 🔑 Chiffrement RSA
├── ✍️ Signature RSA
└── 📱 QR Code
```

## Utilisation

### Chiffrement AES
1. Allez sur l'onglet "🔒 Chiffrement AES"
2. Glissez-déposez un fichier (ou cliquez pour sélectionner)
3. Entrez un mot de passe sécurisé
4. Cliquez "Chiffrer le fichier"
5. Téléchargez le fichier chiffré

### Chiffrement RSA
1. Allez sur l'onglet "🔑 Chiffrement RSA"
2. Sélectionnez un petit fichier (< 200 bytes)
3. Cliquez "Chiffrer le fichier"
4. Téléchargez le résultat

### Signature Numérique
1. Allez sur l'onglet "✍️ Signature RSA"
2. Sélectionnez le fichier à signer
3. Cliquez "Signer le fichier"
4. Téléchargez la signature

### QR Code
1. Allez sur l'onglet "📱 QR Code"
2. Entrez le texte à encoder
3. Cliquez "Générer QR Code" ou "QR Code Signé"
4. Le QR code s'affiche dans l'interface

## Couleurs et Styles

- **Gradient principal**: #667eea → #764ba2 (violet/indigo)
- **Succès**: #4CAF50 (vert)
- **Erreur**: #f8d7da (rouge clair)
- **Info**: #d1ecf1 (bleu clair)
- **Texte**: #333 (gris foncé)

## Fonctionnalités JavaScript

### Utilitaires
- `switchTab(tabName, event)` - Basculer entre onglets
- `showAlert(elementId, message, type)` - Afficher une alerte
- `setupFileDrop(dropZoneId, fileInputId, fileNameId)` - Drag & drop

### Chiffrement AES
- `encryptAES()` - Chiffrer un fichier avec AES
- `resetAES()` - Réinitialiser le formulaire AES

### Chiffrement RSA
- `encryptRSA()` - Chiffrer un fichier avec RSA
- `resetRSA()` - Réinitialiser le formulaire RSA

### Signature
- `signFile()` - Signer un fichier
- `resetSignature()` - Réinitialiser le formulaire

### QR Code
- `generateQR()` - Générer un QR code simple
- `generateSignedQR()` - Générer un QR code signé
- `resetQR()` - Réinitialiser le formulaire

## Routes API Utilisées

```
POST /api/aes/encrypt        - Chiffrer avec AES
POST /api/rsa/encrypt        - Chiffrer avec RSA
POST /api/rsa/sign           - Signer avec RSA
POST /api/qr/simple          - Générer un QR simple
POST /api/qr/signed          - Générer un QR signé
GET  /download/<filename>    - Télécharger un fichier
```

## Améliorations Apportées

✅ **Avant**: Interface basique avec alertes simples
✅ **Après**: 
- Design moderne avec gradient
- Système d'onglets
- Drag & drop intuitif
- Feedback visuel amélioré
- Responsive design
- Gestion des erreurs sophistiquée
- Code JavaScript organisé et commenté

## Compatibilité Navigateur

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Notes Techniques

- Utilise Fetch API pour les requêtes
- CSS Grid et Flexbox pour le layout responsive
- LocalStorage pour le stockage des images QR
- Support du drag & drop natif

## Sécurité

- Les fichiers sont uploadés en HTTPS (en production)
- Les mots de passe ne sont jamais stockés
- Les fichiers chiffrés sont sauvegardés côté serveur
- Limite de taille: 16MB par défaut

---

**Version**: 1.0  
**Développé pour**: Chiffrement sécurisé avec Python/Flask  
**Dernière mise à jour**: 2025

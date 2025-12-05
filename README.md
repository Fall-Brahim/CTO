# 🏋️ CTO - Santé Posturale & Prévention des Blessures

> **Défi Decathlon - Nuit de l'Info 2024**  
> Application Django/DRF pour guider les utilisateurs dans la réalisation correcte de mouvements sportifs et prévenir les blessures.

[![Django](https://img.shields.io/badge/Django-5.1.4-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15.2-red.svg)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/JWT-Authentication-blue.svg)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow.svg)](https://www.python.org/)

---

## 📋 Table des matières

- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Technologies](#-technologies)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [API Documentation](#-api-documentation)
- [Structure du projet](#-structure-du-projet)
- [Tests](#-tests)
- [Contribution](#-contribution)
- [Équipe](#-équipe)

---

## 🎯 Présentation

**CTO (Coach Technique & Optimisation)** est une application web qui aide les sportifs à :
- ✅ Réaliser correctement des mouvements sportifs de base (squats, pompes, yoga, etc.)
- ✅ Prévenir les blessures grâce à des instructions adaptées à leur niveau
- ✅ Suivre leur progression et leurs objectifs
- ✅ Recevoir des recommandations personnalisées

L'application propose un **système de questionnaire intelligent** pour créer un profil sportif personnalisé et fournir des conseils adaptés au niveau de chaque utilisateur (débutant, intermédiaire, avancé).

---

## ✨ Fonctionnalités

### 🔐 Authentification & Gestion utilisateur
- Inscription/Connexion avec JWT (JSON Web Tokens)
- Gestion sécurisée des sessions
- Modification du profil utilisateur
- Changement de mot de passe

### 🏃 Profil Sportif Personnalisé
- Questionnaire de profilage (niveau, objectifs, douleurs)
- Profil sportif unique par utilisateur
- Association de mouvements favoris

### 🎯 Catalogue de Mouvements
- Base de données de mouvements sportifs
- Descriptions détaillées avec images/GIFs
- Liens vers produits Decathlon recommandés
- Recherche par nom de mouvement

### 📚 Instructions Adaptées
- Instructions spécifiques par niveau (débutant/intermédiaire/avancé)
- Conseils personnalisés selon le profil
- Prévention des erreurs courantes

### 📝 Système de Questionnaire
- Questions dynamiques par catégorie
- Réponses multiples avec valeurs associées
- Sauvegarde des réponses utilisateur
- Génération automatique du profil

---

## 🛠️ Technologies

### Backend
- **Django 5.1.4** - Framework web Python
- **Django REST Framework 3.15.2** - API RESTful
- **djangorestframework-simplejwt 5.4.0** - Authentification JWT
- **Pillow 11.0.0** - Gestion des images
- **SQLite** (dev) 

### Architecture
- Architecture REST API
- Authentification stateless (JWT)
- Permissions granulaires par endpoint
- Serializers pour validation des données

---

## 🚀 Installation

### Prérequis
- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

### 1. Cloner le projet

```bash
git clone https://github.com/Fall-Brahim/CTO.git
cd CTO
```

### 2. Créer un environnement virtuel

```bash
# Linux/Mac
python -m venv .env
source .env/bin/activate

# Windows
python -m venv .env
.env\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration de la base de données

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate
```

### 5. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur de développement

```bash
python manage.py runserver
```

L'application sera accessible sur : **http://127.0.0.1:8000**

---

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
# Django Configuration
SECRET_KEY=votre-secret-key-django-super-secrete
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT Configuration
ACCESS_TOKEN_LIFETIME=60  # minutes
REFRESH_TOKEN_LIFETIME=7  # jours
```

### Configuration JWT

Dans `settings.py`, les tokens JWT sont configurés comme suit :
- **Access Token** : 60 minutes
- **Refresh Token** : 7 jours
- **Rotation** : Activée (nouveau refresh token à chaque utilisation)

---

## 📡 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/v1/niveau1/
```

### 🔐 Authentification

#### Inscription
```http
POST /users/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Réponse :**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Connexion
```http
POST /auth/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "SecurePass123!"
}
```

**Réponse :**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Rafraîchir le token
```http
POST /auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Utilisation du token

Pour toutes les requêtes authentifiées, ajoutez le header :
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

### 👤 Utilisateurs

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| `POST` | `/users/register/` | Inscription | ❌ |
| `GET` | `/users/` | Liste des utilisateurs | ✅ |
| `GET` | `/users/{id}/` | Détail d'un utilisateur | ✅ |
| `GET` | `/users/me/` | Profil de l'utilisateur connecté | ✅ |
| `PUT/PATCH` | `/users/update_me/` | Mettre à jour son profil | ✅ |
| `POST` | `/users/change_password/` | Changer son mot de passe | ✅ |

**Exemple - Récupérer son profil :**
```http
GET /users/me/
Authorization: Bearer {access_token}
```

**Exemple - Changer son mot de passe :**
```http
POST /users/change_password/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "old_password": "OldPass123!",
  "new_password": "NewPass456!",
  "new_password2": "NewPass456!"
}
```

---

### 🏋️ Mouvements

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| `GET` | `/movements/` | Liste des mouvements | ✅ |
| `POST` | `/movements/` | Créer un mouvement | ✅ |
| `GET` | `/movements/{id}/` | Détail d'un mouvement | ✅ |
| `PUT/PATCH` | `/movements/{id}/` | Modifier un mouvement | ✅ |
| `DELETE` | `/movements/{id}/` | Supprimer un mouvement | ✅ |
| `GET` | `/movements/by_name/?name=squat` | Rechercher par nom | ✅ |

**Exemple - Créer un mouvement :**
```http
POST /movements/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "Squat",
  "description": "Exercice de base pour les jambes et les fessiers",
  "image_url": "https://example.com/squat.gif",
  "product_url": "https://www.decathlon.fr/p/..."
}
```

---

### 📊 Profils Sportifs

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| `GET` | `/profiles/` | Liste des profils | ✅ |
| `POST` | `/profiles/` | Créer un profil | ✅ |
| `GET` | `/profiles/{id}/` | Détail d'un profil | ✅ |
| `PUT/PATCH` | `/profiles/{id}/` | Modifier un profil | ✅ |
| `DELETE` | `/profiles/{id}/` | Supprimer un profil | ✅ |
| `GET` | `/profiles/{id}/mouvements/` | Mouvements du profil | ✅ |

**Exemple - Créer son profil sportif :**
```http
POST /profiles/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "level": "debutant",
  "objectif": "Améliorer ma posture",
  "douleur": "Mal de dos léger"
}
```

---

### ❓ Questions & Réponses (QCM)

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| `GET` | `/questions/` | Liste des questions | ✅ |
| `POST` | `/questions/` | Créer une question | ✅ |
| `GET` | `/questions/{id}/` | Détail d'une question | ✅ |
| `GET` | `/answers/` | Liste des réponses | ✅ |
| `POST` | `/answers/` | Créer une réponse | ✅ |
| `GET` | `/answers/{id}/` | Détail d'une réponse | ✅ |

---

### ✍️ Réponses Utilisateur

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| `GET` | `/user-responses/` | Mes réponses | ✅ |
| `POST` | `/user-responses/` | Enregistrer une réponse | ✅ |
| `GET` | `/user-responses/by-user/{user_id}/` | Réponses d'un utilisateur | ✅ |

**Exemple - Enregistrer une réponse :**
```http
POST /user-responses/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "question": 1,
  "answer": 3
}
```

---

### 📝 Instructions Mouvements

| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| `GET` | `/movement-instructions/` | Liste des instructions | ✅ |
| `GET` | `/movement-instructions/by-movement-level/?movement={id}&level=debutant` | Instructions filtrées | ✅ |

**Exemple - Récupérer les instructions pour un mouvement :**
```http
GET /movement-instructions/by-movement-level/?movement=1&level=debutant
Authorization: Bearer {access_token}
```

---

## 📁 Structure du projet

```
CTO/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
├── db.sqlite3
│
├── CTO/                      # Configuration Django
│   ├── __init__.py
│   ├── settings.py          # Configuration principale
│   ├── urls.py              # Routes principales
│   └── wsgi.py
│
├── niveau1/                  # Application principale
│   ├── migrations/          # Migrations de base de données
│   ├── __init__.py
│   ├── admin.py            # Interface admin Django
│   ├── apps.py
│   ├── models.py           # Modèles de données
│   ├── serializers.py      # Serializers DRF
│   ├── views.py            # ViewSets API
│   ├── urls.py             # Routes de l'API
│   └── tests.py            # Tests unitaires
│
└── media/                   # Fichiers uploadés
    └── movements/          # Images de mouvements
```

---

## 🧪 Tests

### Lancer les tests

```bash
python manage.py test
```

### Tests manuels avec Postman

1. Importer la collection Postman (disponible dans `/docs/postman_collection.json`)
2. Configurer les variables d'environnement :
   - `base_url` : `http://127.0.0.1:8000/api/v1/niveau1`
   - `access_token` : (généré après login)
   - `refresh_token` : (généré après login)

---

## 🔒 Sécurité

- ✅ Authentification JWT stateless
- ✅ Mots de passe hashés (PBKDF2)
- ✅ Validation des données avec serializers
- ✅ Protection CSRF désactivée pour l'API (JWT)
- ✅ Variables sensibles dans `.env`
- ✅ Rate limiting (à implémenter en production)

### Bonnes pratiques

- Ne **jamais** commit le fichier `.env`
- Ne **jamais** commit `db.sqlite3`
- Utiliser des **tokens temporaires**
- **Rafraîchir** régulièrement les tokens
- Utiliser **HTTPS** en production

---

## 🚀 Déploiement

### Production avec Gunicorn + Nginx

```bash
# Installer Gunicorn
pip install gunicorn

# Lancer l'application
gunicorn CTO.wsgi:application --bind 0.0.0.0:8000
```

### Variables d'environnement pour production

```env
DEBUG=False
ALLOWED_HOSTS=votredomaine.com,www.votredomaine.com
SECRET_KEY=votre-secret-key-super-complexe-et-longue
```

---

## 🤝 Contribution

Les contributions sont les bienvenues !

### Workflow Git

```bash
# 1. Créer une branche pour votre fonctionnalité
git checkout -b feature/ma-nouvelle-fonctionnalite

# 2. Faire vos modifications et commits
git add .
git commit -m "feat: Add new feature"

# 3. Pousser votre branche
git push origin feature/ma-nouvelle-fonctionnalite

# 4. Créer une Pull Request sur GitHub
```

### Conventions de commit

- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage du code
- `refactor:` Refactoring
- `test:` Ajout de tests
- `chore:` Tâches de maintenance

---

## 👥 Équipe

Projet réalisé dans le cadre de la **Nuit de l'Info 2025** - Défi Decathlon

### Contributeurs
- Votre équipe ici

---

## 📄 Licence

Ce projet est développé dans le cadre d'un événement académique (Nuit de l'Info 2025).

---

## 📞 Contact & Support

- 🐛 **Issues** : [GitHub Issues](https://github.com/Fall-Brahim/CTO/issues)
- 📧 **Email** : fallbrahimalioun@gmail.
- 🌐 **Site** : [Nuit de l'Info](https://www.nuitdelinfo.com/)

---

## 🎉 Remerciements

- **Decathlon Digital** pour le défi inspirant
- **Nuit de l'Info 2025** pour l'organisation
- La communauté **Django** et **DRF**

---

<div align="center">
  
**⭐ Si ce projet vous plaît, n'hésitez pas à lui donner une étoile sur GitHub ! ⭐**

Made with ❤️ during Nuit de l'Info 2025

</div>

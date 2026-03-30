# DÉMARRAGE RAPIDE

Cette plateforme est complètement configurée. Voici les étapes pour commencer.

## 1️⃣ Configuration de la base de données

### Option A : Script SQL automatique
```bash
# Créer la base de données
mysql -u root -p < create_database.sql

# Entrez votre mot de passe MySQL quand demandé
```

### Option B : Commandes MySQL manuelles
```sql
mysql -u root -p

CREATE DATABASE projet_suivi_rdc CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

## 2️⃣ Configuration du fichier .env

Modifiez `.env` avec vos paramètres MySQL:
```env
DB_NAME=projet_suivi_rdc
DB_USER=root
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=3306
```

## 3️⃣ Initialisation du projet

### Méthode rapide (automatisée) - RECOMMANDÉE
```bash
python setup.py
```

### Méthode manuelle
```bash
# Migration de la base de données
python manage.py makemigrations
python manage.py migrate

# Création de l'utilisateur admin
python manage.py createsuperuser
```

## 4️⃣ Lancer le serveur

```bash
python manage.py runserver
```

## 5️⃣ Accès à l'application

- **Interface utilisateur** : http://localhost:8000/
- **Admin Django** : http://localhost:8000/admin/
- **Identifiants par défaut** (si vous avez run setup.py) :
  - Utilisateur : `admin`
  - Mot de passe : `admin123`

⚠️ Changez le mot de passe après la première connexion!

## 📁 Structure du projet

```
c:\Users\Dell\projet django\
├── .env                     ← Configurer ici
├── README.md               ← Documentation complète
├── INSTALLATION.md         ← Guide d'installation détaillé
├── DOCUMENTATION.md        ← API et architecture
├── create_database.sql     ← Script de création BD
├── setup.py               ← Script d'initialisation

├── projet_suivi/          ← Configuration Django
├── utilisateurs/          ← Gestion des utilisateurs
├── projets/              ← Gestion des projets
├── financement/          ← Gestion du financement
├── templates/            ← Fichiers HTML
├── static/              ← CSS, JavaScript
└── media/               ← Fichiers uploadés
```

## 🔑 Fonctionnalités principales

✅ **Gestion des projets** - Création, modification, suivi
✅ **Financement** - Suivi des sources et versements
✅ **Dépenses** - Enregistrement avec justificatifs
✅ **Activités** - Gestion des étapes du projet
✅ **Rapports** - Génération de rapports de suivi
✅ **Utilisateurs** - Gestion des rôles et permissions
✅ **Admin Django** - Interface d'administration complète

## 🛠️ Commandes essentielles

```bash
# Lancer le serveur
python manage.py runserver

# Faire les migrations
python manage.py makemigrations
python manage.py migrate

# Créer un utilisateur admin
python manage.py createsuperuser

# Shell Django (console)
python manage.py shell

# Vérifier la configuration
python manage.py check

# Collecter les fichiers statiques
python manage.py collectstatic

# Vider le cache
python manage.py clear_cache
```

## 🆘 Dépannage

### Erreur MySQL
```
Error: Can't connect to MySQL server on 'localhost'
```
**Solution** : Vérifiez que MySQL est en cours d'exécution

### Erreur de module
```
ModuleNotFoundError: No module named 'mysqlclient'
```
**Solution** : 
```bash
pip install --force-reinstall mysqlclient
```

### Erreur de base de données
Si vous avez une erreur lors des migrations:
```bash
# Vérifiez la configuration dans .env
# Recreez la base de données
python setup.py
```

## ✨ Prochaines étapes

1. ✅ Lancer le serveur
2. 👤 Créer des utilisateurs
3. 📊 Créer un premier projet
4. 💰 Ajouter des financements
5. 📋 Enregistrer les dépenses
6. 📈 Consulter les rapports

## 📚 Documentation

- **README.md** - Vue d'ensemble complète
- **INSTALLATION.md** - Guide d'installation détaillé
- **DOCUMENTATION.md** - Architecture et API
- **django.com** - Documentation officielle Django

## 🚀 Production

Pour passer en production:

1. Changez `DEBUG=False` au lieu de `True` dans `.env`
2. Générez une nouvelle `SECRET_KEY`
3. Configurez `ALLOWED_HOSTS` correctement
4. Mettez en place HTTPS
5. Configurez une vraie serveur (Gunicorn, Nginx)
6. Sauvegardez régulièrement la base de données

## 📧 Support

Pour des problèmes:
1. Consultez la documentation (README.md, INSTALLATION.md)
2. Vérifiez que MySQL fonctionne
3. Vérifiez les logs Django
4. Consultez la documentation Django officielle

---

**Créé avec ❤️ pour la gestion de projets financés en RDC**


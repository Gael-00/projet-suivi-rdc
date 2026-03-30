# Guide d'Installation Rapide

## Prérequis
- Python 3.9+
- MySQL 5.7+ ou MariaDB
- Git (optionnel)

## Étapes d'installation

### 1. Préparation de la base de données MySQL

```sql
-- Connectez-vous à MySQL
mysql -u root -p

-- Créer la base de données
CREATE DATABASE projet_suivi_rdc CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Créer un utilisateur pour la base de données (optionnel)
CREATE USER 'projet_user'@'localhost' IDENTIFIED BY 'votre_mot_de_passe_securise';
GRANT ALL PRIVILEGES ON projet_suivi_rdc.* TO 'projet_user'@'localhost';
FLUSH PRIVILEGES;

-- Quitter MySQL
EXIT;
```

### 2. Configuration du projet

```bash
# Naviguer dans le répertoire du projet
cd "c:\Users\Dell\projet django"

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel (Windows)
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Configuration des variables d'environnement

Éditez le fichier `.env` :

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuration MySQL
DB_ENGINE=django.db.backends.mysql
DB_NAME=projet_suivi_rdc
DB_USER=root          # ou projet_user
DB_PASSWORD=          # Mettez votre mot de passe
DB_HOST=localhost
DB_PORT=3306
```

### 4. Initialiser la base de données

```bash
# Lancer le script d'initialisation (automatise les migrations)
python setup.py

# OU faire les migrations manuellement
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Lancer le serveur

```bash
python manage.py runserver
```

Accédez à l'application :
- **Application** : http://localhost:8000/
- **Admin Django** : http://localhost:8000/admin/
- **Identifiants par défaut** : admin / admin123

## Dépannage

### Erreur : "Can't connect to MySQL server"

```bash
# Vérifiez que MySQL est en cours d'exécution (Windows)
# Services > MySQL80 (ou votre version)

# Vérifiez les paramètres dans .env
# Testez la connexion
mysql -u root -p -h localhost

# Assurez-vous que la base de données existe
mysql -u root -p -e "SHOW DATABASES;"
```

### Erreur : "ModuleNotFoundError: No module named 'mysqlclient'"

```bash
# Réinstallez mysqlclient
pip install --force-reinstall mysqlclient
```

### Erreur : "django.core.exceptions.ImproperlyConfigured"

```bash
# Assurez-vous que les variables d'environnement sont correctes dans .env
# Vérifiez les paramètres de la base de données
python manage.py check
```

## Structure du projet créée

```
c:\Users\Dell\projet django\
├── .env                          # Configuration d'environnement
├── manage.py                     # Gestion Django
├── requirements.txt              # Dépendances
├── setup.py                      # Script d'initialisation
├── README.md                     # Documentation
├── INSTALLATION.md              # Guide d'installation
├── projet_suivi/                # Configuration du projet
│   ├── settings.py              # Paramètres Django
│   ├── urls.py                  # Routage
│   ├── wsgi.py
│   └── asgi.py
├── utilisateurs/                # Application utilisateurs
│   ├── models.py                # Modèle Utilisateur
│   ├── views.py                 # Vues
│   ├── urls.py                  # Routes
│   ├── forms.py                 # Formulaires
│   ├── admin.py                 # Admin
│   └── migrations/
├── projets/                     # Application projets
│   ├── models.py                # Modèles projets
│   ├── views.py                 # Vues
│   ├── urls.py                  # Routes
│   ├── admin.py                 # Admin
│   └── migrations/
├── financement/                 # Application financement
│   ├── views.py                 # Vues
│   ├── urls.py                  # Routes
│   └── admin.py                 # Admin
├── templates/                   # Templates HTML
│   ├── base.html                # Template de base
│   ├── index.html               # Page d'accueil
│   ├── dashboard.html           # Tableau de bord
│   └── utilisateurs/
│       └── login.html           # Formulaire de connexion
├── static/                      # Fichiers statiques
├── media/                       # Fichiers uploadés
└── venv/                        # Environnement virtuel
```

## Commandes utiles

```bash
# Activer l'environnement virtuel
venv\Scripts\activate

# Faire les migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver

# Collecter les fichiers statiques
python manage.py collectstatic

# Shell Django
python manage.py shell

# Vérifier la configuration
python manage.py check

# Désactiver l'environnement virtuel
deactivate
```

## Prochaines étapes

1. **Connexion** : Accédez à http://localhost:8000/utilisateurs/connexion/
2. **Admin** : Gérez les utilisateurs et projets à http://localhost:8000/admin/
3. **Création de projets** : Cliquez sur "Nouveau projet" pour commencer
4. **Financement** : Ajoutez des sources de financement
5. **Rapports** : Consultez les rapports de financement

## Support

En cas de problème, consultez :
- La documentation Django : https://docs.djangoproject.com/
- Le README.md du projet
- Les logs Django dans la console

## Notes de sécurité

⚠️ **IMPORTANT POUR LA PRODUCTION** :
- Changez `SECRET_KEY` dans settings.py
- Définissez `DEBUG=False`
- Configurez `ALLOWED_HOSTS` correctement
- Utilisez une base de données MySQL sécurisée
- Changez les mots de passe par défaut
- Configurez HTTPS
- Mettez en place une sauvegarde régulière


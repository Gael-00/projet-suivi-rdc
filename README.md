# Plateforme de Gestion de Suivi de Projets Financés - RDC

Plateforme complète pour le suivi et la gestion des projets financés en République Démocratique du Congo (RDC), développée avec Django et MySQL.

## Architecture

Le projet utilise le pattern MTV (Model-Template-View) de Django :
- **Modèles (Models)** : Structure des données des projets, financements, dépenses et activités
- **Vues (Views)** : Logique métier pour gérer les opérations CRUD
- **Templates** : Interface utilisateur pour l'affichage des données

## Applications

### 1. **utilisateurs** - Gestion des utilisateurs
- Authentification personnalisée
- Rôles et permissions (Admin, Responsable de projet, Financier, etc.)
- Gestion des profils utilisateurs
- **Modèles** :
  - `Utilisateur` : Utilisateur personnalisé avec rôles et institution

### 2. **projets** - Gestion des projets
- Création et suivi des projets financés
- Gestion des dépenses
- Suivi des activités et étapes
- Générations de rapports
- **Modèles** :
  - `Projet` : Projet financé avec budget et statut
  - `Financement` : Source de financement (gouvernement, ONG, banque, etc.)
  - `Depense` : Dépense du projet avec justificatif
  - `Activite` : Activité/étape du projet
  - `Rapport` : Rapport de suivi trimestriel, semestriel, annuel

### 3. **financement** - Gestion du financement
- Suivi des sources de financement
- Versement des fonds
- État des financements
- Rapports de financement

## Configuration

### Prérequis
- Python 3.9+
- MySQL 5.7+
- pip (gestionnaire de paquets Python)

### Installation

1. **Cloner le projet (ou extraire les fichiers)**

2. **Créer un environnement virtuel** :
```bash
python -m venv venv
venv\Scripts\activate  # Sur Windows
source venv/bin/activate  # Sur Linux/Mac
```

3. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

4. **Configurer la base de données** :
- Éditer le fichier `.env` avec vos paramètres MySQL :
```env
DB_NAME=projet_suivi_rdc
DB_USER=root
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=3306
```

5. **Faire les migrations** :
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Créer un utilisateur administrateur** :
```bash
python manage.py createsuperuser
```

7. **Lancer le serveur de développement** :
```bash
python manage.py runserver
```

Accédez à l'application à `http://localhost:8000/`

## Utilisation

### Connexion
- Accédez à `/utilisateurs/connexion/`
- Utilisez les identifiants de l'utilisateur administrateur créé

### Administration Django
- Accédez à `/admin/` pour l'interface d'administration
- Gérez les projets, financements, dépenses et utilisateurs

### Pages principales
- **Liste des projets** : `/projets/` - Vue de tous les projets avec filtres
- **Détails du projet** : `/projets/<id>/` - Vue détaillée d'un projet
- **Gestion du financement** : `/financement/` - Suivi des sources de financement
- **Rapports** : `/financement/rapport/` - État du financement global

## Rôles et Permissions

1. **Admin** : Accès complet à tout le système
2. **Responsable de projet** : Création et gestion de projets
3. **Financier** : Gestion des financements et dépenses
4. **Auditeur** : Visualisation et audit
5. **Chef d'activité** : Gestion des activités
6. **Consultant** : Consultation des données
7. **Visualisateur** : Accès en lecture seule

## Modèles de données

### Projet
- Code projet (unique)
- Titre et description
- Budget total et montant financé
- Dates (début, fin prévue, fin réelle)
- Statut (planifié, en cours, terminé, annulé)
- Responsable
- Province et localisation

### Financement
- Type (gouvernement, banque, ONG, secteur privé)
- Nom du financeur
- Montant et pourcentage
- Dates (accord, versement prévu, versement réel)
- Statut du versement
- Référence d'accord

### Dépense
- Description et catégorie
- Montant et date
- Bénéficiaire
- Document justificatif
- Référence de paiement

### Activité
- Nom et description
- Dates (début/fin prévues et réelles)
- Statut et responsable
- Pourcentage de complétion
- Résultats attendus et réalisés

### Rapport
- Titre et type (trimestri, semestriel, annuel, final, audit)
- Date du rapport
- Contenu et fichier
- Redacteur et approbateur

## API Django

Toutes les données sont accessibles via l'interface Django admin :
- `/admin/utilisateurs/utilisateur/`
- `/admin/projets/projet/`
- `/admin/projets/financement/`
- `/admin/projets/depense/`
- `/admin/projets/activite/`
- `/admin/projets/rapport/`

## Structure des répertoires

```
projet_suivi/
├── .env                          # Configuration d'environnement
├── manage.py                     # Script de gestion Django
├── requirements.txt              # Dépendances Python
├── projet_suivi/                 # Configuration du projet
│   ├── settings.py               # Paramètres Django
│   ├── urls.py                   # Routage principal
│   ├── wsgi.py                   # Configuration WSGI
│   └── asgi.py                   # Configuration ASGI
├── utilisateurs/                 # Application utilisateurs
│   ├── models.py                 # Modèle Utilisateur
│   ├── views.py                  # Vues d'authentification
│   ├── urls.py                   # Routes utilisateurs
│   ├── forms.py                  # Formulaires
│   └── admin.py                  # Interface admin
├── projets/                      # Application projets
│   ├── models.py                 # Modèles (Projet, Financement, etc.)
│   ├── views.py                  # Vues CRUD
│   ├── urls.py                   # Routes projets
│   └── admin.py                  # Interface admin
├── financement/                  # Application financement
│   ├── views.py                  # Vues financement
│   ├── urls.py                   # Routes financement
│   └── admin.py                  # Interface admin
├── templates/                    # Modèles HTML
├── static/                       # Fichiers statiques (CSS, JS)
└── media/                        # Fichiers uploadés
```

## Fonctionnalités principales

✅ Authentification et gestion des rôles
✅ Création et suivi des projets
✅ Gestion des dépenses avec justificatifs
✅ Suivi des sources de financement
✅ Gestion des activités/étapes
✅ Génération de rapports
✅ Filtrage et recherche avancée
✅ Interface d'administration Django complète
✅ Support multi-utilisateur
✅ Validation des données

## Variables d'environnement (.env)

```
SECRET_KEY=votre_clé_secrète
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.mysql
DB_NAME=projet_suivi_rdc
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

## Support et aide

Pour des questions ou des problèmes :
1. Consultez la documentation Django : https://docs.djangoproject.com/
2. Vérifiez les paramètres de configuration dans settings.py
3. Assurez-vous que MySQL est en cours d'exécution et accessible

## Licence

Ce projet est fourni tel quel pour la gestion de projets financés par la RDC.

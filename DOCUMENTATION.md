# Documentation de la Plateforme

## Vue d'ensemble

Cette plateforme offre une gestion complète du suivi de projets financés en République Démocratique du Congo. Elle est construite avec Django et MySQL, utilisant le pattern MTV (Model-Template-View).

## Architecture MTV

### Modèles (Models)
Les modèles représentent la structure des données:

#### Application `utilisateurs`
- **Utilisateur** : Utilisateur du système avec rôles et permissions
  - username, email, password
  - first_name, last_name
  - role (admin, responsable_projet, financier, etc.)
  - institution (minfin, minplan, etc.)
  - telephone, adresse, ville, province
  - photo, date_creation, date_modification

#### Application `projets`
- **Projet** : Projet financé principal
  - code_projet (unique)
  - titre, description, objectif
  - date_debut, date_fin_prevue, date_fin_reelle
  - statut (planifie, en_cours, en_attente, termine, annule)
  - responsable (ForeignKey → Utilisateur)
  - budget_total, montant_finance, devise
  - province, ville, zone_geographique
  - created_by (ForeignKey → Utilisateur)

- **Financement** : Source de financement
  - type_financement (gouvernement, banque_developpement, ong, secteur_prive, partenaire, autre)
  - nom_financeur
  - montant, pourcentage
  - date_accord, date_versement_prevue, date_versement_reelle
  - statut_versement (prevu, verse, retard, annule)
  - reference_accord, notes
  - projet (ForeignKey → Projet)

- **Depense** : Dépense enregistrée
  - description, categorie (personnel, equipement, infrastructure, transport, fournitures, formation, audit, autre)
  - montant, date_depense
  - beneficiaire, reference_paiement
  - document_justificatif (fichier)
  - enregistre_par (ForeignKey → Utilisateur)
  - projet (ForeignKey → Projet)

- **Activite** : Activité/étape du projet
  - nom, description
  - date_debut_prevue, date_fin_prevue, date_debut_reelle, date_fin_reelle
  - statut (non_demarree, en_cours, completee, suspendue)
  - responsable (ForeignKey → Utilisateur)
  - pourcentage_completion (0-100)
  - resultats_attendus, resultats_realises
  - projet (ForeignKey → Projet)

- **Rapport** : Rapport de suivi
  - titre, type_rapport (trimestri, semestriel, annuel, final, audit)
  - date_rapport, contenu, fichier
  - redacteur (ForeignKey → Utilisateur)
  - approuve_par (ForeignKey → Utilisateur, nullable)
  - date_approbation
  - projet (ForeignKey → Projet)

### Vues (Views)
Les vues gèrent la logique métier et les requêtes HTTP.

#### Utilisateurs
- LoginView : Authentification
- LogoutView : Déconnexion
- UtilisateurListView : Liste des utilisateurs (admin)
- UtilisateurDetailView : Profil d'un utilisateur
- UtilisateurCreateView : Créer un utilisateur (admin)
- UtilisateurUpdateView : Modifier un utilisateur
- UtilisateurDeleteView : Supprimer un utilisateur (admin)
- mon_profil : Vue du profil personnalisé

#### Projets
- ProjetListView : Liste avec filtres et recherche
- ProjetDetailView : Détails complets d'un projet
- ProjetCreateView : Créer un nouveau projet
- ProjetUpdateView : Modifier un projet
- ProjetDeleteView : Supprimer un projet (admin)
- FinancementListView : Financements d'un projet
- DepenseListView : Dépenses d'un projet
- DepenseCreateView : Enregistrer une dépense

#### Financement
- FinancementListView : Liste de tous les financements
- FinancementCreateView : Ajouter un financement
- FinancementUpdateView : Modifier un financement
- FinancementDeleteView : Supprimer un financement (admin)
- rapport_financement : Générer un rapport

### Templates (Affichage)
Les templates définissent l'interface utilisateur. Les principaux templates:

- **base.html** : Template de base avec navigation et footer
- **index.html** : Page d'accueil
- **dashboard.html** : Tableau de bord
- **utilisateurs/login.html** : Formulaire de connexion

## Routes principales

```
POST /utilisateurs/connexion/                          # Connexion
GET  /utilisateurs/deconnexion/                        # Déconnexion
GET  /utilisateurs/                                    # Liste des utilisateurs
GET  /utilisateurs/<id>/                               # Profil d'un utilisateur
POST /utilisateurs/creer/                              # Créer un utilisateur
POST /utilisateurs/<id>/editer/                        # Modifier un utilisateur
POST /utilisateurs/<id>/supprimer/                     # Supprimer un utilisateur
GET  /utilisateurs/profil/                             # Mon profil

GET  /projets/                                         # Liste des projets
GET  /projets/<id>/                                    # Détails d'un projet
POST /projets/creer/                                   # Créer un projet
POST /projets/<id>/editer/                             # Modifier un projet
POST /projets/<id>/supprimer/                          # Supprimer un projet

GET  /projets/projet/<projet_id>/financements/        # Financements du projet
GET  /projets/projet/<projet_id>/depenses/            # Dépenses du projet
POST /projets/projet/<projet_id>/depenses/creer/      # Enregistrer une dépense

GET  /financement/                                     # Liste des financements
POST /financement/projet/<projet_id>/creer/           # Ajouter un financement
POST /financement/<id>/editer/                         # Modifier un financement
POST /financement/<id>/supprimer/                      # Supprimer un financement
GET  /financement/rapport/                             # Rapport de financement

GET  /admin/                                           # Interface d'administration Django
```

## Rôles et Permissions

### Admin
- Accès complet à toutes les fonctionnalités
- Gestion des utilisateurs
- Suppression de projets
- Accès à l'admin Django

### Responsable de projet
- Créer et modifier ses projets
- Gérer les financements de ses projets
- Enregistrer les dépenses
- Consulter les rapports

### Financier
- Gérer tous les financements
- Enregistrer les dépenses
- Consulter les rapports
- Créer des projets

### Auditeur
- Accès en lecture seule
- Consulter tous les projets
- Consulter tous les financements
- Générer des rapports

### Chef d'activité
- Gérer les activités de ses projets
- Consulter les dépenses
- Créer les rapports

### Consultant
- Consultation des données
- Génération de rapports

### Visualisateur
- Accès en lecture seule
- Consultation limitée

## Filtres et Recherche

### Projets
- Filtrer par statut (planifié, en_cours, en_attente, terminé, annulé)
- Filtrer par province
- Recherche par code_projet, titre ou description

### Financements
- Filtrer par type (gouvernement, banque, ONG, secteur_privé, etc.)
- Filtrer par statut de versement
- Rechercher par nom du financeur ou code_projet

### Dépenses
- Filtrer par catégorie
- Filtrer par date
- Rechercher par description

## Fonctionnalités avancées

### Authentification
- Login/Logout personnalisé
- Rôles et permissions
- Protection des vues

### Gestion des données
- Validation des données
- Fichiers justificatifs
- Calculs automatiques (budget restant, pourcentage, retards)

### Rapports
- Rapport de financement global
- Statistiques par projet
- Suivi des versements

### Sécurité
- CSRF protection
- Admin Django sécurisé
- Contrôle d'accès par rôle

## Méthodes utiles des modèles

### Projet
```python
projet.budget_restant()           # Calcule le budget restant
projet.pourcentage_financement()  # Pourcentage financé
projet.is_en_retard()             # Vérifie si en retard
```

### Financement
```python
financement.is_en_retard()        # Vérifie versement en retard
```

## Configuration Django

### Settings importants
- `AUTH_USER_MODEL = 'utilisateurs.Utilisateur'`
- `LANGUAGE_CODE = 'fr-fr'`
- `TIME_ZONE = 'Africa/Kinshasa'`
- `DATABASES` configuré pour MySQL
- `INSTALLED_APPS` inclut les 3 applications

### Variables d'environnement (.env)
- `SECRET_KEY` : Clé secrète Django
- `DEBUG` : Mode debug
- `ALLOWED_HOSTS` : Hôtes autorisés
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

## Maintenance

### Backups
```bash
# Exporter les données
python manage.py dumpdata > backup.json

# Importer les données
python manage.py loaddata backup.json
```

### Logs
- Logs Django dans la console
- Logs des requêtes HTTP
- Logs d'erreur au niveau du serveur

## Support et développement

Pour développer une nouvelle fonctionnalité:

1. Créer un modèle dans `models.py`
2. Créer une vue dans `views.py`
3. Enregistrer dans `admin.py`
4. Ajouter les routes dans `urls.py`
5. Créer les templates HTML
6. Faire les migrations: `python manage.py makemigrations && python manage.py migrate`


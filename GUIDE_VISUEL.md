# GUIDE VISUEL DE LA PLATEFORME

## 🏗️ Architecture générale

```
┌─────────────────────────────────────────────────────────────┐
│                    PLATEFORME DE GESTION                    │
│            Projets Financés - RDC (Django + MySQL)          │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                    ▼         ▼         ▼
        ┌──────────────┐  ┌────────┐  ┌───────────┐
        │ Utilisateurs │  │Projets │  │Financement│
        │  (App 1)     │  │(App 2) │  │  (App 3)  │
        └──────────────┘  └────────┘  └───────────┘
                    │         │         │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │     MySQL BD      │
                    │  projet_suivi_rdc │
                    └───────────────────┘
```

## 👤 Cycle de vie de l'utilisateur

```
[ Nouveau utilisateur ]
        │
        ▼
    Créé par admin
        │
        ├──────────────────────┬──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
    [ Responsable ]   [ Financier ]         [ Auditeur ]
    de projet          Gère le         Consulte les
    Crée/modifie      financement     données
    les projets       et dépenses
        │                  │                  │
        └──────────┬───────┴─────────┬────────┘
                   │                 │
                   ▼                 ▼
            Dashboard & Rapports
```

## 📊 Flux de création d'un projet

```
                    ┌─────────────────┐
                    │  Admin authentifié
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Clic "Nouveau  │
                    │  projet"        │
                    └────────┬────────┘
                             │
                    ┌────────▼────────────────────┐
                    │  Formulaire de création     │
                    │  - Code projet              │
                    │  - Titre & Description      │
                    │  - Budget total             │
                    │  - Dates (début/fin)        │
                    │  - Responsable              │
                    │  - Province/Ville          │
                    └────────┬────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  Validation de  │
                    │  données        │
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
          NON              OUI               ERREUR
           │                 │                 │
       Erreurs          Sauvegarde    Afficher messages
        affichées        en BD
                            │
                    ┌────────▼────────┐
                    │  Projet créé!  │
                    │  Redirection   │
                    │  vers détails  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────────┐
                    │ Possibilités:       │
                    │ + Ajouter financements
                    │ + Créer activités   │
                    │ + Enregistrer dépenses
                    │ + Générer rapports  │
                    └─────────────────────┘
```

## 💰 Flux de gestion du financement

```
Créer un financement pour le projet
        │
        ├─ Type (Gouvernement, ONG, Banque...)
        ├─ Nom du financeur
        ├─ Montant (en CDF)
        ├─ Pourcentage du budget
        ├─ Date d'accord
        └─ Date de versement prévue
        │
        ▼
Enregistrer en BD
        │
        ▼
Suivi du versement
        │
        ├─ Prévu  (Date future)
        ├─ Versé  (Versement effectué)
        ├─ Retard (Versement tardif)
        └─ Annulé (Versement annulé)
        │
        ▼
Mise à jour du budget du projet
        │
        ├─ Montant financé ↑
        ├─ Budget restant ↓
        └─ % de financement ↑
        │
        ▼
Rapport de financement généré
```

## 📋 Structure des rôles et accès

```
                        ADMIN
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
    Gestion infra       Accès complet   Rapports
    • Utilisateurs      • Tous projets   • Global
    • BD                • Tous rôles     • Détaillés
    • Sécurité          • Admin Django   • Exports
        │
        ├─ Responsable Projet
        │   │
        │   ├─ Ses projets uniquement
        │   ├─ Modifier projet
        │   ├─ Ajouter activités
        │   └─ Voir rapport
        │
        ├─ Financier
        │   │
        │   ├─ Tous les financements
        │   ├─ Enregistrer dépenses
        │   ├─ Modifier versements
        │   └─ Rapport financier
        │
        └─ Auditeur
            │
            ├─ Lecture seule
            ├─ Tous les projets
            ├─ Consultation rapports
            └─ Aucune modification

```

## 📈 Relations entre les modèles

```
                        ┌──────────────┐
                        │ UTILISATEUR  │
                        │ - username   │
                        │ - role       │
                        │ - institution│
                        └──────┬───────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
           ┌─────────┐  ┌──────────┐  ┌──────────────┐
           │ PROJET  │  │ACTIVITE  │  │  RAPPORT    │
           │- code   │  │- nom     │  │- titre      │
           │- titre  │  │- statut  │  │- type       │
           │- budget │  │- %compl. │  │- contenu    │
           │- dates  │  │- resp.   │  │- redacteur  │
           └────┬────┘  └──────────┘  └──────────────┘
                │
        ┌───────┼───────┐
        │       │       │
        ▼       ▼       ▼
    ┌────────────┐ ┌──────────┐
    │FINANCEMENT │ │ DEPENSE  │
    │- type      │ │- montant │
    │- montant   │ │- categorie
    │- date vers │ │- date    │
    │- statut    │ │- enregistre_par
    └────────────┘ └──────────┘
```

## 🔐 Flux d'authentification

```
                  [ Visiteur ]
                       │
                    ▼──────▼
          [ Clic sur "Connexion" ]
                       │
            ┌──────────▼──────────┐
            │  Formulaire Login   │
            │  - Username         │
            │  - Mot de passe     │
            └──────────┬──────────┘
                       │
            ┌──────────▼──────────┐
            │  Vérif. credentials │
            └──────────┬──────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
      ERREUR         SUCCÈS        VERROUILLÉ
        │              │              │
        ▼              ▼              ▼
    Message        Session      Message
    d'erreur       créée        compte bloqué
                      │
                      ▼
            [ Utilisateur connecté ]
                      │
                      ▼
            [ Dashboard/Accueil ]
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
    Projets     Financements    Rapports
```

## 🎯 Cas d'usage principal

```
                   RESPONSABLE DE PROJET
                           │
                ┌──────────┬┴────────┬──────────┐
                │          │        │          │
                ▼          ▼        ▼          ▼
             Crée       Ajoute    Enregistre  Génère
             Projet     Finan.    Dépenses    Rapport
                │          │         │         │
                └──────────┼─────────┼────────┘
                           │
                ┌──────────▼──────────┐
                │  Suivi du projet   │
                │  - Budget         │
                │  - Progression    │
                │  - Statut         │
                │  - Retards        │
                └───────────────────┘
                           │
                          ▼
                ┌──────────────────────┐
                │  Rapport mensuel     │
                │  - Financements reçus│
                │  - Dépenses         │
                │  - Activités        │
                │  - Problèmes        │
                └──────────────────────┘
```

## 📚 Flux de navigation

```
┌─────────────────────────────────────────────────────────────┐
│                      BARRE NAVIGATION                       │
│  Logo │ Projets │ Financements │ (Admin│) │ Profil│Décon. │
└──────────────────────────────────────────────────────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
      Projets Menu   Financement    Utilisateurs
            │         Menu              Menu
            │              │              │
     ┌──────┴──────┐  ┌────┴────┐  ┌────┴────┐
     │             │  │         │  │         │
  Liste     Créer  Voir    Rapport Liste   Profil
  Détails   Nouveau Tous  Financ.  Détails Modifier
  Modifier  Éditer Filtrer Export   Créer  Supprimer
  Supprimer         Chercher (admin) (admin)
```

## 🗄️ Cycle de vie des données

```
Saisie utilisateur
        │
        ├─ Validation (côté serveur)
        │
        ├─ Sauvegarde en BD
        │
        ├─ Enregistrement log
        │
        ├─ Calculs associés
        │   • Budget restant
        │   • Pourcentage
        │   • Détection de retards
        │
        ├─ Génération de rapports
        │
        └─ Affichage mise à jour
```

---

Cette plateforme est conçue pour simplifier la gestion des projets financés en RDC 🇨🇩


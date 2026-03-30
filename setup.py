#!/usr/bin/env python
"""
Script d'initialisation de la plateforme de gestion des projets financés.
Lance les étapes de configuration initiale.
"""

import os
import sys
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet_suivi.settings')
django.setup()

from django.core.management import call_command
from utilisateurs.models import Utilisateur

def setup_base_de_donnees():
    """Applique toutes les migrations"""
    print("\n🗄️  Applying database migrations...")
    try:
        call_command('migrate')
        print("✅ Migrations appliquées avec succès!")
    except Exception as e:
        print(f"❌ Erreur lors de l'application des migrations: {e}")
        return False
    return True

def creer_utilisateur_admin():
    """Crée un utilisateur administrateur par défaut"""
    print("\n👤 Creating admin user...")
    
    if Utilisateur.objects.filter(username='admin').exists():
        print("ℹ️  L'utilisateur admin existe déjà")
        return True
    
    try:
        admin = Utilisateur.objects.create_superuser(
            username='admin',
            email='admin@projet-rdc.local',
            password='admin123',
            first_name='Administrateur',
            last_name='Système',
            role='admin',
            institution='minfin'
        )
        print(f"✅ Utilisateur admin créé: {admin.username}")
        print("   Email: admin@projet-rdc.local")
        print("   Mot de passe: admin123")
        print("⚠️  Changez le mot de passe après la première connexion!")
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'utilisateur admin: {e}")
        return False
    return True

def collecter_fichiers_statiques():
    """Collecte les fichiers statiques"""
    print("\n📦 Collecting static files...")
    try:
        call_command('collectstatic', '--noinput')
        print("✅ Fichiers statiques collectés!")
    except Exception as e:
        print(f"⚠️  Warning: {e}")
    return True

def main():
    print("\n" + "="*60)
    print("🚀 INITIALISATION DE LA PLATEFORME")
    print("Plateforme de Gestion de Suivi de Projets Financés - RDC")
    print("="*60)
    
    # Étapes d'initialisation
    steps = [
        ("Base de données", setup_base_de_donnees),
        ("Utilisateur administrateur", creer_utilisateur_admin),
        ("Fichiers statiques", collecter_fichiers_statiques),
    ]
    
    success = True
    for step_name, step_func in steps:
        if not step_func():
            success = False
            print(f"❌ {step_name} échoué")
            break
    
    print("\n" + "="*60)
    if success:
        print("✅ INITIALISATION RÉUSSIE!")
        print("\n📝 Prochaines étapes:")
        print("   1. Lancez le serveur: python manage.py runserver")
        print("   2. Accédez à: http://localhost:8000/")
        print("   3. Admin: http://localhost:8000/admin/")
        print("   4. Connexion: admin / admin123")
    else:
        print("❌ INITIALISATION INCOMPLÈTE")
        print("Veuillez vérifier les messages d'erreur ci-dessus")
    print("="*60 + "\n")
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())

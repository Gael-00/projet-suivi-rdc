#!/usr/bin/env python
# Script pour resets la BD complètement

import mysql.connector
import os
import sys

try:
    # Connexion à MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''
    )
    
    cursor = conn.cursor()
    
    # Supprimer la BD
    cursor.execute('DROP DATABASE IF EXISTS projet_suivi_rdc')
    print("✅ Ancienn base supprimée")
    
    # Créer nouvelle BD
    cursor.execute('''
        CREATE DATABASE projet_suivi_rdc 
        CHARACTER SET utf8mb4 
        COLLATE utf8mb4_unicode_ci
    ''')
    print("✅ Nouvelle base créée")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# Supprimer les fichiers de migration problématiques
import shutil

for app in ['utilisateurs', 'projets', 'financement']:
    migration_path = f'{app}/migrations'
    if os.path.exists(migration_path):
        # Garder le __init__.py
        init_file = f'{app}/migrations/__init__.py'
        shutil.rmtree(migration_path)
        os.makedirs(migration_path)
        open(init_file, 'w').close()
        print(f"✅ Migrations de {app} nettoyées")

print("\n✅ Base de données nettoyée et prête!")
print("Maintenant, lancez: python manage.py makemigrations && python manage.py migrate")

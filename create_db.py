#!/usr/bin/env python
# Script pour créer la base de données

import sys

try:
    import mysql.connector
    
    # Connexion à MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''  # WAMP n'a pas de mot de passe par défaut
    )
    
    cursor = conn.cursor()
    
    # Créer la base de données
    cursor.execute('''
        CREATE DATABASE IF NOT EXISTS projet_suivi_rdc 
        CHARACTER SET utf8mb4 
        COLLATE utf8mb4_unicode_ci
    ''')
    
    print("✅ Base de données 'projet_suivi_rdc' créée avec succès!")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    print("\nVérifiez que:")
    print("1. WAMP Server est démarré (icône verte)")
    print("2. MySQL fonctionne correctement")
    sys.exit(1)

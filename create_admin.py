#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet_suivi.settings')

import django
django.setup()

from utilisateurs.models import Utilisateur

# Créer l'utilisateur admin
admin, created = Utilisateur.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@example.com',
        'first_name': 'Admin',
        'last_name': 'Système',
        'is_staff': True,
        'is_superuser': True,
        'role': 'admin',
        'institution': 'minfin',
    }
)

if created:
    admin.set_password('admin123')
    admin.save()
    print("✅ Utilisateur admin créé!")
    print("   Username: admin")
    print("   Password: admin123")
else:
    print("ℹ️ Utilisateur admin existe déjà")

print("\n✅ Tout est prêt!")
print("\nPour lancer le serveur, tapez:")
print("python manage.py runserver")

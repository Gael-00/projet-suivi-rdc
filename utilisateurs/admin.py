from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email', 'telephone', 'photo')}),
        ('Adresse', {'fields': ('adresse', 'ville', 'province')}),
        ('Rôle et institution', {'fields': ('role', 'institution', 'est_actif')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    list_display = ('username', 'get_full_name', 'email', 'role', 'institution', 'est_actif')
    list_filter = ('role', 'institution', 'est_actif', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('first_name', 'last_name')

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Utilisateur(AbstractUser):
    """Modèle d'utilisateur personnalisé"""
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('responsable_projet', 'Responsable de projet'),
        ('financier', 'Gestionnaire financier'),
        ('auditeur', 'Auditeur'),
        ('chef_activite', 'Chef d\'activité'),
        ('consultant', 'Consultant'),
        ('visualisateur', 'Visualisateur'),
    ]
    
    INSTITUTION_CHOICES = [
        ('minfin', 'Ministère des Finances'),
        ('minplan', 'Ministère du Plan'),
        ('minbudget', 'Ministère du Budget'),
        ('pnud', 'PNUD'),
        ('banque_mondiale', 'Banque Mondiale'),
        ('autre', 'Autre'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='visualisateur')
    institution = models.CharField(max_length=50, choices=INSTITUTION_CHOICES)
    telephone = models.CharField(
        max_length=20, 
        blank=True, 
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Entrez un numéro valide')]
    )
    adresse = models.CharField(max_length=255, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='photos_utilisateurs/', blank=True, null=True)
    
    # Statut et permissions
    est_actif = models.BooleanField(default=True)
    date_derniere_connexion = models.DateTimeField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

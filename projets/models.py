from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from utilisateurs.models import Utilisateur

class Projet(models.Model):
    """Modèle représentant un projet financé"""
    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('en_attente', 'En attente'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    
    code_projet = models.CharField(max_length=50, unique=True)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    objectif = models.TextField(blank=True, null=True)
    date_debut = models.DateField()
    date_fin_prevue = models.DateField()
    date_fin_reelle = models.DateField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifie')
    responsable = models.ForeignKey(Utilisateur, on_delete=models.PROTECT, related_name='projets_responsable')
    
    # Budget et financement
    budget_total = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    montant_finance = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    devise = models.CharField(max_length=3, default='CDF')  # Franc congolais
    
    # Localisation
    province = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    zone_geographique = models.CharField(max_length=100, blank=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, related_name='projets_createurs')
    
    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.code_projet} - {self.titre}"
    
    def budget_restant(self):
        """Calcule le budget restant"""
        return self.budget_total - self.montant_finance
    
    def pourcentage_financement(self):
        """Calcule le pourcentage de financement"""
        if self.budget_total == 0:
            return 0
        return (self.montant_finance / self.budget_total) * 100
    
    def is_en_retard(self):
        """Vérifie si le projet est en retard"""
        if self.statut == 'termine':
            return self.date_fin_reelle > self.date_fin_prevue
        return timezone.now().date() > self.date_fin_prevue and self.statut != 'termine'


class Financement(models.Model):
    """Modèle représentant une source de financement"""
    TYPE_FINANCEMENT_CHOICES = [
        ('gouvernement', 'Gouvernement RDC'),
        ('banque_developpement', 'Banque de développement'),
        ('ong', 'ONG / Organisation internationale'),
        ('secteur_prive', 'Secteur privé'),
        ('partenaire', 'Partenaire bilatéral'),
        ('autre', 'Autre'),
    ]
    
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='financements')
    type_financement = models.CharField(max_length=30, choices=TYPE_FINANCEMENT_CHOICES)
    nom_financeur = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    pourcentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    date_accord = models.DateField()
    date_versement_prevue = models.DateField()
    date_versement_reelle = models.DateField(blank=True, null=True)
    statut_versement = models.CharField(
        max_length=20,
        choices=[
            ('prevu', 'Prévu'),
            ('verse', 'Versé'),
            ('retard', 'En retard'),
            ('annule', 'Annulé'),
        ],
        default='prevu'
    )
    reference_accord = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Financement"
        verbose_name_plural = "Financements"
        unique_together = ('projet', 'nom_financeur')
        ordering = ['projet', '-date_accord']
    
    def __str__(self):
        return f"{self.projet.code_projet} - {self.nom_financeur} ({self.montant})"
    
    def is_en_retard(self):
        """Vérifie si le versement est en retard"""
        if self.date_versement_reelle:
            return self.date_versement_reelle > self.date_versement_prevue
        return timezone.now().date() > self.date_versement_prevue and self.statut_versement != 'verse'


class Depense(models.Model):
    """Modèle représentant une dépense du projet"""
    CATEGORIE_CHOICES = [
        ('personnel', 'Personnel'),
        ('equipement', 'Équipement'),
        ('infrastructure', 'Infrastructure'),
        ('transport', 'Transport'),
        ('fournitures', 'Fournitures'),
        ('formation', 'Formation'),
        ('audit', 'Audit'),
        ('autre', 'Autre'),
    ]
    
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='depenses')
    description = models.CharField(max_length=255)
    categorie = models.CharField(max_length=30, choices=CATEGORIE_CHOICES)
    montant = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    date_depense = models.DateField()
    beneficiaire = models.CharField(max_length=255, blank=True)
    reference_paiement = models.CharField(max_length=100, blank=True)
    document_justificatif = models.FileField(upload_to='justificatifs/', blank=True, null=True)
    enregistre_par = models.ForeignKey(Utilisateur, on_delete=models.PROTECT, related_name='depenses_enregistrees')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Dépense"
        verbose_name_plural = "Dépenses"
        ordering = ['-date_depense']
    
    def __str__(self):
        return f"{self.projet.code_projet} - {self.description} ({self.montant})"


class Activite(models.Model):
    """Modèle représentant une activité/étape du projet"""
    STATUT_ACTIVITE_CHOICES = [
        ('non_demarree', 'Non démarrée'),
        ('en_cours', 'En cours'),
        ('completee', 'Complétée'),
        ('suspendue', 'Suspendue'),
    ]
    
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='activites')
    nom = models.CharField(max_length=255)
    description = models.TextField()
    date_debut_prevue = models.DateField()
    date_fin_prevue = models.DateField()
    date_debut_reelle = models.DateField(blank=True, null=True)
    date_fin_reelle = models.DateField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_ACTIVITE_CHOICES, default='non_demarree')
    responsable = models.ForeignKey(Utilisateur, on_delete=models.PROTECT, related_name='activites_responsable')
    pourcentage_completion = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    resultats_attendus = models.TextField(blank=True)
    resultats_realises = models.TextField(blank=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['projet', 'date_debut_prevue']
    
    def __str__(self):
        return f"{self.projet.code_projet} - {self.nom}"


class Rapport(models.Model):
    """Modèle représentant un rapport de suivi"""
    TYPE_RAPPORT_CHOICES = [
        ('trimestri', 'Trimestriel'),
        ('semestriel', 'Semestriel'),
        ('annuel', 'Annuel'),
        ('final', 'Final'),
        ('audit', 'Audit'),
    ]
    
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name='rapports')
    titre = models.CharField(max_length=255)
    type_rapport = models.CharField(max_length=20, choices=TYPE_RAPPORT_CHOICES)
    date_rapport = models.DateField()
    contenu = models.TextField()
    fichier = models.FileField(upload_to='rapports/', blank=True, null=True)
    redacteur = models.ForeignKey(Utilisateur, on_delete=models.PROTECT, related_name='rapports_rediges')
    approuve_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True, related_name='rapports_approuves')
    date_approbation = models.DateField(blank=True, null=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Rapport"
        verbose_name_plural = "Rapports"
        ordering = ['-date_rapport']
    
    def __str__(self):
        return f"{self.projet.code_projet} - {self.titre} ({self.date_rapport})"

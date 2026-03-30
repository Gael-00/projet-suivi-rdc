from django.contrib import admin
from .models import Projet, Financement, Depense, Activite, Rapport


@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('code_projet', 'titre', 'statut', 'responsable', 'budget_total', 'montant_finance', 'date_debut', 'date_fin_prevue')
    list_filter = ('statut', 'province', 'date_creation')
    search_fields = ('code_projet', 'titre', 'description')
    readonly_fields = ('date_creation', 'date_modification')
    fieldsets = (
        ('Informations générales', {'fields': ('code_projet', 'titre', 'description', 'objectif')}),
        ('Dates', {'fields': ('date_debut', 'date_fin_prevue', 'date_fin_reelle')}),
        ('Statut et responsable', {'fields': ('statut', 'responsable')}),
        ('Budget et financement', {'fields': ('budget_total', 'montant_finance', 'devise')}),
        ('Localisation', {'fields': ('province', 'ville', 'zone_geographique')}),
        ('Métadonnées', {'fields': ('created_by', 'date_creation', 'date_modification')}),
    )


@admin.register(Financement)
class FinancementAdmin(admin.ModelAdmin):
    list_display = ('projet', 'nom_financeur', 'type_financement', 'montant', 'statut_versement', 'date_accord')
    list_filter = ('type_financement', 'statut_versement', 'date_accord')
    search_fields = ('nom_financeur', 'projet__code_projet')
    readonly_fields = ('date_creation', 'date_modification')
    fieldsets = (
        ('Projet et financeur', {'fields': ('projet', 'type_financement', 'nom_financeur')}),
        ('Financement', {'fields': ('montant', 'pourcentage', 'reference_accord')}),
        ('Dates de versement', {'fields': ('date_accord', 'date_versement_prevue', 'date_versement_reelle')}),
        ('Statut', {'fields': ('statut_versement',)}),
        ('Remarques', {'fields': ('notes',)}),
        ('Métadonnées', {'fields': ('date_creation', 'date_modification')}),
    )


@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ('projet', 'description', 'categorie', 'montant', 'date_depense', 'beneficiaire')
    list_filter = ('categorie', 'date_depense', 'projet')
    search_fields = ('description', 'beneficiaire', 'projet__code_projet')
    readonly_fields = ('date_creation', 'date_modification', 'enregistre_par')
    fieldsets = (
        ('Projet et description', {'fields': ('projet', 'description', 'categorie')}),
        ('Montant et date', {'fields': ('montant', 'date_depense')}),
        ('Bénéficiaire et justificatif', {'fields': ('beneficiaire', 'reference_paiement', 'document_justificatif')}),
        ('Enregistrement', {'fields': ('enregistre_par', 'date_creation', 'date_modification')}),
    )

    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une nouvelle dépense
            obj.enregistre_par = request.user
        super().save_model(request, obj, form, change)


@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('projet', 'nom', 'statut', 'responsable', 'pourcentage_completion', 'date_debut_prevue', 'date_fin_prevue')
    list_filter = ('statut', 'date_debut_prevue', 'projet')
    search_fields = ('nom', 'description', 'projet__code_projet')
    readonly_fields = ('date_creation', 'date_modification')


@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display = ('projet', 'titre', 'type_rapport', 'date_rapport', 'redacteur', 'approuve_par')
    list_filter = ('type_rapport', 'date_rapport', 'projet')
    search_fields = ('titre', 'contenu', 'projet__code_projet')
    readonly_fields = ('date_creation', 'date_modification')

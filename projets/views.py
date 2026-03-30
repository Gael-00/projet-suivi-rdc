from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from django.utils import timezone
from .models import Projet, Financement, Depense, Activite, Rapport
from utilisateurs.models import Utilisateur


class ProjetListView(LoginRequiredMixin, ListView):
    """Liste de tous les projets avec filtres"""
    model = Projet
    template_name = 'projets/projet_list.html'
    context_object_name = 'projets'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Projet.objects.all()
        
        # Filtres
        statut = self.request.GET.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        
        province = self.request.GET.get('province')
        if province:
            queryset = queryset.filter(province=province)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(code_projet__icontains=search) |
                Q(titre__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.order_by('-date_creation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques
        context['total_projets'] = Projet.objects.count()
        context['projets_en_cours'] = Projet.objects.filter(statut='en_cours').count()
        context['budget_total'] = Projet.objects.aggregate(Sum('budget_total'))['budget_total__sum'] or 0
        context['montant_finance'] = Projet.objects.aggregate(Sum('montant_finance'))['montant_finance__sum'] or 0
        
        return context


class ProjetDetailView(LoginRequiredMixin, DetailView):
    """Détails d'un projet"""
    model = Projet
    template_name = 'projets/projet_detail.html'
    context_object_name = 'projet'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projet = self.get_object()
        
        context['financements'] = Financement.objects.filter(projet=projet)
        context['depenses'] = Depense.objects.filter(projet=projet)
        context['activites'] = Activite.objects.filter(projet=projet)
        context['rapports'] = Rapport.objects.filter(projet=projet)
        
        # Calculs
        context['total_depenses'] = Depense.objects.filter(projet=projet).aggregate(Sum('montant'))['montant__sum'] or 0
        context['total_financement'] = Financement.objects.filter(projet=projet).aggregate(Sum('montant'))['montant__sum'] or 0
        
        return context


class ProjetCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Créer un nouveau projet"""
    model = Projet
    template_name = 'projets/projet_form.html'
    fields = ['code_projet', 'titre', 'description', 'objectif', 'date_debut', 'date_fin_prevue',
              'responsable', 'budget_total', 'devise', 'province', 'ville', 'zone_geographique']
    success_url = reverse_lazy('projets:projet-list')
    
    def test_func(self):
        return self.request.user.role in ['admin', 'responsable_projet']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProjetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Mettre à jour un projet"""
    model = Projet
    template_name = 'projets/projet_form.html'
    fields = ['code_projet', 'titre', 'description', 'objectif', 'statut', 'date_debut', 
              'date_fin_prevue', 'date_fin_reelle', 'responsable', 'budget_total', 'montant_finance',
              'devise', 'province', 'ville', 'zone_geographique']
    success_url = reverse_lazy('projets:projet-list')
    
    def test_func(self):
        projet = self.get_object()
        return self.request.user.role in ['admin', 'responsable_projet'] or self.request.user == projet.responsable


class ProjetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Supprimer un projet"""
    model = Projet
    template_name = 'projets/projet_confirm_delete.html'
    success_url = reverse_lazy('projets:projet-list')
    
    def test_func(self):
        return self.request.user.role == 'admin'


class FinancementListView(LoginRequiredMixin, ListView):
    """Liste des financements d'un projet"""
    model = Financement
    template_name = 'projets/financement_list.html'
    context_object_name = 'financements'
    
    def get_queryset(self):
        projet_id = self.kwargs.get('projet_id')
        return Financement.objects.filter(projet_id=projet_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projet'] = get_object_or_404(Projet, id=self.kwargs.get('projet_id'))
        return context


class DepenseListView(LoginRequiredMixin, ListView):
    """Liste des dépenses d'un projet"""
    model = Depense
    template_name = 'projets/depense_list.html'
    context_object_name = 'depenses'
    paginate_by = 20
    
    def get_queryset(self):
        projet_id = self.kwargs.get('projet_id')
        return Depense.objects.filter(projet_id=projet_id).order_by('-date_depense')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projet = get_object_or_404(Projet, id=self.kwargs.get('projet_id'))
        context['projet'] = projet
        context['total_depenses'] = Depense.objects.filter(projet=projet).aggregate(Sum('montant'))['montant__sum'] or 0
        return context


class DepenseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Enregistrer une dépense"""
    model = Depense
    template_name = 'projets/depense_form.html'
    fields = ['description', 'categorie', 'montant', 'date_depense', 'beneficiaire', 
              'reference_paiement', 'document_justificatif']
    
    def test_func(self):
        return self.request.user.role in ['admin', 'responsable_projet', 'financier']
    
    def form_valid(self, form):
        form.instance.projet = get_object_or_404(Projet, id=self.kwargs.get('projet_id'))
        form.instance.enregistre_par = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('projets:depense-list', kwargs={'projet_id': self.kwargs.get('projet_id')})

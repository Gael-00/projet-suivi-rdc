from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Sum, Q
from projets.models import Financement, Projet


class FinancementListView(LoginRequiredMixin, ListView):
    """Liste de tous les financements"""
    model = Financement
    template_name = 'financement/financement_list.html'
    context_object_name = 'financements'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Financement.objects.all()
        
        # Filtres
        type_financement = self.request.GET.get('type')
        if type_financement:
            queryset = queryset.filter(type_financement=type_financement)
        
        statut = self.request.GET.get('statut')
        if statut:
            queryset = queryset.filter(statut_versement=statut)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nom_financeur__icontains=search) |
                Q(projet__code_projet__icontains=search)
            )
        
        return queryset.order_by('-date_accord')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistiques
        context['total_financement'] = Financement.objects.aggregate(Sum('montant'))['montant__sum'] or 0
        context['financement_verse'] = Financement.objects.filter(statut_versement='verse').aggregate(Sum('montant'))['montant__sum'] or 0
        context['financement_en_retard'] = Financement.objects.filter(statut_versement='retard').count()
        
        return context


class FinancementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Créer une source de financement"""
    model = Financement
    template_name = 'financement/financement_form.html'
    fields = ['type_financement', 'nom_financeur', 'montant', 'pourcentage', 'date_accord',
              'date_versement_prevue', 'reference_accord', 'notes']
    success_url = reverse_lazy('financement:financement-list')
    
    def test_func(self):
        return self.request.user.role in ['admin', 'financier']
    
    def form_valid(self, form):
        projet_id = self.kwargs.get('projet_id')
        form.instance.projet = get_object_or_404(Projet, id=projet_id)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projet'] = get_object_or_404(Projet, id=self.kwargs.get('projet_id'))
        return context


class FinancementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Mettre à jour une source de financement"""
    model = Financement
    template_name = 'financement/financement_form.html'
    fields = ['type_financement', 'nom_financeur', 'montant', 'pourcentage', 'date_accord',
              'date_versement_prevue', 'date_versement_reelle', 'statut_versement', 'reference_accord', 'notes']
    success_url = reverse_lazy('financement:financement-list')
    
    def test_func(self):
        return self.request.user.role in ['admin', 'financier']


class FinancementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Supprimer une source de financement"""
    model = Financement
    template_name = 'financement/financement_confirm_delete.html'
    success_url = reverse_lazy('financement:financement-list')
    
    def test_func(self):
        return self.request.user.role == 'admin'


def rapport_financement(request):
    """Rapport de financement"""
    financements = Financement.objects.all()
    
    context = {
        'total_finance': financements.aggregate(Sum('montant'))['montant__sum'] or 0,
        'financement_verse': financements.filter(statut_versement='verse').aggregate(Sum('montant'))['montant__sum'] or 0,
        'financement_en_attente': financements.filter(statut_versement='prevu').aggregate(Sum('montant'))['montant__sum'] or 0,
        'financement_en_retard': financements.filter(statut_versement='retard').aggregate(Sum('montant'))['montant__sum'] or 0,
        'par_type': financements.values('type_financement').annotate(total=Sum('montant')).order_by('-total'),
    }
    
    return render(request, 'financement/rapport_financement.html', context)

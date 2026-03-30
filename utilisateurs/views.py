from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Utilisateur
from .forms import UtilisateurCreationForm, UtilisateurChangeForm


class UtilisateurLoginView(LoginView):
    """Vue de connexion"""
    template_name = 'utilisateurs/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')


class UtilisateurLogoutView(LoginRequiredMixin, LogoutView):
    """Vue de déconnexion"""
    next_page = reverse_lazy('utilisateurs:login')


class UtilisateurListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Liste de tous les utilisateurs"""
    model = Utilisateur
    template_name = 'utilisateurs/utilisateur_list.html'
    context_object_name = 'utilisateurs'
    paginate_by = 20
    
    def test_func(self):
        return self.request.user.role == 'admin'
    
    def get_queryset(self):
        queryset = Utilisateur.objects.all()
        
        # Filtres
        role = self.request.GET.get('role')
        if role:
            queryset = queryset.filter(role=role)
        
        institution = self.request.GET.get('institution')
        if institution:
            queryset = queryset.filter(institution=institution)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        return queryset.order_by('first_name', 'last_name')


class UtilisateurDetailView(LoginRequiredMixin, DetailView):
    """Profil d'un utilisateur"""
    model = Utilisateur
    template_name = 'utilisateurs/utilisateur_detail.html'
    context_object_name = 'utilisateur'


class UtilisateurCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Créer un nouvel utilisateur"""
    model = Utilisateur
    form_class = UtilisateurCreationForm
    template_name = 'utilisateurs/utilisateur_form.html'
    success_url = reverse_lazy('utilisateurs:utilisateur-list')
    
    def test_func(self):
        return self.request.user.role == 'admin'


class UtilisateurUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Mettre à jour un utilisateur"""
    model = Utilisateur
    form_class = UtilisateurChangeForm
    template_name = 'utilisateurs/utilisateur_form.html'
    success_url = reverse_lazy('utilisateurs:utilisateur-list')
    
    def test_func(self):
        utilisateur = self.get_object()
        return self.request.user.role == 'admin' or self.request.user == utilisateur


class UtilisateurDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Supprimer un utilisateur"""
    model = Utilisateur
    template_name = 'utilisateurs/utilisateur_confirm_delete.html'
    success_url = reverse_lazy('utilisateurs:utilisateur-list')
    
    def test_func(self):
        return self.request.user.role == 'admin'


def mon_profil(request):
    """Vue du profil personnelisé"""
    utilisateur = request.user
    return render(request, 'utilisateurs/mon_profil.html', {'utilisateur': utilisateur})

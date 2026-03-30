from django.urls import path
from . import views

app_name = 'utilisateurs'

urlpatterns = [
    # Authentification
    path('connexion/', views.UtilisateurLoginView.as_view(), name='login'),
    path('deconnexion/', views.UtilisateurLogoutView.as_view(), name='logout'),
    
    # Utilisateurs
    path('', views.UtilisateurListView.as_view(), name='utilisateur-list'),
    path('<int:pk>/', views.UtilisateurDetailView.as_view(), name='utilisateur-detail'),
    path('creer/', views.UtilisateurCreateView.as_view(), name='utilisateur-create'),
    path('<int:pk>/editer/', views.UtilisateurUpdateView.as_view(), name='utilisateur-update'),
    path('<int:pk>/supprimer/', views.UtilisateurDeleteView.as_view(), name='utilisateur-delete'),
    path('profil/', views.mon_profil, name='mon-profil'),
]

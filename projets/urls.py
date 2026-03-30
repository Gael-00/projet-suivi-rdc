from django.urls import path
from . import views

app_name = 'projets'

urlpatterns = [
    # Projets
    path('', views.ProjetListView.as_view(), name='projet-list'),
    path('<int:pk>/', views.ProjetDetailView.as_view(), name='projet-detail'),
    path('creer/', views.ProjetCreateView.as_view(), name='projet-create'),
    path('<int:pk>/editer/', views.ProjetUpdateView.as_view(), name='projet-update'),
    path('<int:pk>/supprimer/', views.ProjetDeleteView.as_view(), name='projet-delete'),
    
    # Financements
    path('projet/<int:projet_id>/financements/', views.FinancementListView.as_view(), name='financement-list'),
    
    # Dépenses
    path('projet/<int:projet_id>/depenses/', views.DepenseListView.as_view(), name='depense-list'),
    path('projet/<int:projet_id>/depenses/creer/', views.DepenseCreateView.as_view(), name='depense-create'),
]

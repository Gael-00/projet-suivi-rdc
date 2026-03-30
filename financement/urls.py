from django.urls import path
from . import views

app_name = 'financement'

urlpatterns = [
    # Financements
    path('', views.FinancementListView.as_view(), name='financement-list'),
    path('projet/<int:projet_id>/creer/', views.FinancementCreateView.as_view(), name='financement-create'),
    path('<int:pk>/editer/', views.FinancementUpdateView.as_view(), name='financement-update'),
    path('<int:pk>/supprimer/', views.FinancementDeleteView.as_view(), name='financement-delete'),
    
    # Rapports
    path('rapport/', views.rapport_financement, name='rapport-financement'),
]

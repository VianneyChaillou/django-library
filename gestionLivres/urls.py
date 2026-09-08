from django.urls import path
from . import views

urlpatterns = [
    path('listeLivres/', views.liste_livre, name='listeLivres'),
    path('ajouterLivre/', views.ajouterLivre, name='ajouterLivre'),
    path('modifierLivre/<int:livre_id>/', views.modifierLivre, name='modifierLivre'),
    path('supprimerLivre/<int:livre_id>/', views.supprimerLivre, name='supprimerLivre'),
    path('ajouterEmprunt/', views.ajouterEmprunt, name='ajouterEmprunt'),
    path('emprunts/', views.listeEmprunts, name='listeEmprunts'),
    path('rendreEmprunt/<int:emprunt_id>/', views.rendre_emprunt, name='rendreEmprunt'),
    path('mesEmprunts/', views.empruntUser, name='mesEmprunts'),
]
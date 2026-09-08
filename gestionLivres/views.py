from django.shortcuts import render, redirect
from bd.models import Livre, Emprunt
from .forms import LivreFormulaire, EmpruntForm
from .decorateurs import adminRequired
from django.http import HttpResponseForbidden
from django.utils import timezone
from datetime import date
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Vue publique
@login_required
def liste_livre(request):
    livres = Livre.objects.all()
    return render(request, 'listeLivres.html', {'livres': livres})


@adminRequired # Vue réservée aux admins
@login_required
def ajouterLivre(request):
    if request.method == 'POST': #si l'utilisateur à soumis le formulaire
        form = LivreFormulaire(request.POST)
        if form.is_valid():
            form.save() # Sauvegarde le livre dans la base de données
            return redirect('listeLivres') # Redirige vers la liste des livres après l’ajout
    else:
        form = LivreFormulaire()
    return render(request, 'ajouterLivre.html', {'form': form})


@adminRequired
@login_required
def modifierLivre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id) # essai de récupérer le livre par son ID, sinon 404
    if request.method == 'POST': 
        form = LivreFormulaire(request.POST, instance=livre) # crée un formulaire avec les données du livre existant
        if form.is_valid(): # si le formulaire est valide
            form.save()
            return redirect('listeLivres')
    else:
        form = LivreFormulaire(instance=livre) # crée un formulaire avec les données du livre existant pour pré-remplir le formulaire
    return render(request, 'modifierLivre.html', {'form': form, 'livre': livre})


@adminRequired
@login_required
def supprimerLivre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    if request.method == 'POST':
        livre.delete()
        return redirect('listeLivres')
    return render(request, 'supprimerLivre.html', {'livre': livre})

@adminRequired
@login_required
def ajouterEmprunt(request):
    if request.method == 'POST':
        form = EmpruntForm(request.POST)
        if form.is_valid():
            emprunt = form.save(commit=False)
            emprunt.date_emprunt = timezone.now().date()
            emprunt.date_retour = emprunt.date_emprunt + timedelta(days=15)
            emprunt.rendu = False
            emprunt.save()

            # on decremente le stock 
            emprunt.livre.save()

            return redirect('listeEmprunts')
    else:
        form = EmpruntForm()

    return render(request, 'ajouterEmprunt.html', {'form': form})


@adminRequired
@login_required
def rendre_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)
    # Ne pas traiter deux fois un retour
    if emprunt.date_retour is None: #pour vérifier si l'emprunt n'a pas déjà été rendu
        emprunt.date_retour = timezone.now()
        emprunt.save()
        emprunt.livre.nb_exemplaires += 1
        emprunt.livre.save() 
    
    return redirect('listeEmprunts')

@adminRequired
@login_required
def listeEmprunts(request):

    today = date.today()

    # Tous les emprunts non rendus
    emprunts_actifs = Emprunt.objects.filter(rendu=False)

    # Parmi eux, ceux en retard
    emprunts_en_retard = emprunts_actifs.filter(date_retour__lte=today) #lte : date au plus égale a ajourd'hui

    # Historique des retours
    historique = Emprunt.objects.filter(rendu=True)

    return render(request, 'listeEmprunts.html', {
        'emprunts_actifs': emprunts_actifs, 
        'emprunts_en_retard_ids': list(emprunts_en_retard.values_list('id', flat=True)), #pour récupérer les id des emprunt en retard
        'historique': historique
    })


@adminRequired
@login_required
def rendre_emprunt(request, emprunt_id):

    emprunt = get_object_or_404(Emprunt, id=emprunt_id)

    if request.method == 'POST':  #si le bouton "confirmer le retour" est cliquer
        emprunt.date_retour = timezone.now().date()
        emprunt.rendu = True
        emprunt.save()

        emprunt.livre.nb_exemplaires += 1
        emprunt.livre.save()

        return redirect('listeEmprunts')

    return render(request, 'confirmerRetour.html', {'emprunt': emprunt})

@login_required
def empruntUser(request):
    
    today = date.today()
    
    # Emprunts actifs de l'utilisateur
    emprunts_actifs = Emprunt.objects.filter(
        utilisateur=request.user,
        rendu=False
    )
    
    # Emprunts en retard de l'utilisateur
    emprunts_en_retard = emprunts_actifs.filter(
        date_retour__lte=today
    )
    
    # Historique des emprunts de l'utilisateur
    historique = Emprunt.objects.filter(
        utilisateur=request.user,
        rendu=True
    )
    
    return render(request, 'EmpruntUser.html', {
        'emprunts_actifs': emprunts_actifs,
        'emprunts_en_retard_ids': list(emprunts_en_retard.values_list('id', flat=True)),
        'historique': historique
    })

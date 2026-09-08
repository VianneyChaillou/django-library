from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from bd.models import Utilisateur
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'login.html')

        try:
            utilisateur = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            messages.error(request, "Email ou mot de passe incorrect.")
            return render(request, 'login.html')

        if not utilisateur.check_password(password):
            messages.error(request, "Email ou mot de passe incorrect.")
            return render(request, 'login.html')

        login(request, utilisateur)
        print("... :", request.user.is_authenticated)
        return redirect('/')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login') #Rediriger vers la page de connexion
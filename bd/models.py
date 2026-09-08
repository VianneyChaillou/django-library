from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

class Utilisateur(AbstractUser) :
    username = None
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=100)
    datePublication = models.DateField()
    nb_exemplaires = models.IntegerField(default=1)

    def __str__(self): 
        return f"{self.titre} - {self.auteur} ({self.datePublication.strftime('%d/%m/%Y')}) - {self.nb_exemplaires}"
    

class Emprunt(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    date_emprunt = models.DateField(default=timezone.now)
    date_retour = models.DateField(blank=True, null=True)
    rendu = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.date_retour:
            self.date_retour = self.date_emprunt + timedelta(days=15)

        # Vérifie et décrémente le stock
        if self.pk is None:  # On ne décrémente que si c'est un nouvel emprunt
            if self.livre.nb_exemplaires <= 0:
                raise ValueError("Aucun exemplaire disponible pour ce livre.")
            self.livre.nb_exemplaires -= 1
            self.livre.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.utilisateur.email} → {self.livre.titre}"
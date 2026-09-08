from django import forms
from bd.models import Livre, Emprunt

class LivreFormulaire(forms.ModelForm):
    datePublication = forms.DateField(
        input_formats=['%d/%m/%Y'], #impose le format JJ/MM/AAAA
        widget=forms.DateInput(
            format='%d/%m/%Y',
            attrs={'placeholder': 'JJ/MM/AAAA'} #afficher un texte griser pour guider
        )
    )

    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'datePublication', 'nb_exemplaires']


class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['utilisateur', 'livre']  # date_emprunt et date_retour gérés auto
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        # Ne proposer que les livres disponibles
        self.fields['livre'].queryset = Livre.objects.filter(nb_exemplaires__gt=0)
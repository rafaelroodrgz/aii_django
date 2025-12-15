from django import forms
from main.models import FormatoDeEmision as FE

class BusquedaPorFormatoForm(forms.Form):
    formatoDeEmision = forms.ModelChoiceField(label="Seleccione el formato de emisión", queryset=FE.objects.all())
    
class AnimeBusquedaForm(forms.Form):
    idAnime = forms.CharField(label="Id de Anime", widget=forms.TextInput, required=True)
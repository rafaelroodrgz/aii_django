from django import forms
from main.models import FormatoDeEmision as FE

class BusquedaPorFormatoForm(forms.Form):
    formatoDeEmision = forms.ModelChoiceField(label="Seleccione el formato de emisión", queryset=FE.objects.all())
    

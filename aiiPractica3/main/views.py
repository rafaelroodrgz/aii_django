from django.shortcuts import render, redirect
from django.conf import settings
from main.populateDB import populate
from main.models import Anime
from main.forms import BusquedaPorFormatoForm


# Create your views here.
def index(request):
    return render(request, 'index.html',{'STATIC_URL':settings.STATIC_URL})


def carga(request):
    if request.method=='POST':
        if 'Aceptar' in request.POST:      
            a, b = populate()
            mensaje="Se han almacenado: " + str(a) +" Animes, " + str(b) +" Puntuaciones"
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')

def animesPorFormato(request):
    formulario = BusquedaPorFormatoForm()
    animes = None
    
    if request.method=='POST':
        formulario = BusquedaPorFormatoForm(request.POST)      
        if formulario.is_valid():
            animes = Anime.objects.filter(formatoDeEmision=formulario.cleaned_data['formatoDeEmision'])
            
    return render(request, 'animesPorFormato.html', {'formulario':formulario, 'animes':animes})
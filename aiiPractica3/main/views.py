from django.shortcuts import render, redirect
from django.conf import settings
from main.populateDB import populate
from main.models import Anime
from main.forms import BusquedaPorFormatoForm

from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches
from main.models import Puntuacion, Anime
from django.http.response import HttpResponseRedirect
from django.db.models import Avg, Count
import shelve

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
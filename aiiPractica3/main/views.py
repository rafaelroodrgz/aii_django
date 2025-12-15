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

def animesPorFormato(request):
    formulario = BusquedaPorFormatoForm()
    animes = None
    
    if request.method=='POST':
        formulario = BusquedaPorFormatoForm(request.POST)      
        if formulario.is_valid():
            animes = Anime.objects.filter(formatoDeEmision=formulario.cleaned_data['formatoDeEmision'])
            
    return render(request, 'animesPorFormato.html', {'formulario':formulario, 'animes':animes})

def loadRS(request):
    loadDict()
    return HttpResponseRedirect('/index.html')

def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Puntuacion.objects.all()
    for ra in ratings:
        user = int(ra.idUsuario)
        itemid = int(ra.anime.animeid)
        rating = float(ra.puntuacion)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()

def mostrar_animes_mas_puntuaciones(request):
#     ANIMES MÁS POPULARES. Muestre los tres animes que más 
# puntuaciones han recibido (Título y número de puntuaciones recibidas). Para cada uno 
# de ellos mostrar también los tres animes que más se le parecen (Título y similitud), 
# usando la distancia Euclidea como medida de similitud. 
    animes = Anime.objects.annotate(num_rating=Count('puntuacion__puntuacion')).order_by('-num_rating')[:3]
    return render(request, 'animes_mas_puntuados.html', {'animes':animes, 'STATIC_URL':settings.STATIC_URL})
from django.shortcuts import render, redirect
from django.conf import settings
from main.populateDB import populate
from main.forms import BusquedaPorFormatoForm

from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendations, getRecommendedItems, topMatches
from main.models import Puntuacion, Anime
from django.http.response import HttpResponseRedirect
from django.db.models import Avg, Count
import shelve
from django.db.models import Count
import math

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



def calcular_distancia_euclidea(puntos_anime_a, puntos_anime_b):
    usuarios_comunes = set(puntos_anime_a.keys()) & set(puntos_anime_b.keys())
    
    if not usuarios_comunes:
        return float('inf') 
    suma_cuadrados = sum(
        pow(puntos_anime_a[usuario] - puntos_anime_b[usuario], 2) 
        for usuario in usuarios_comunes
    )
    return math.sqrt(suma_cuadrados)


def mostrar_animes_mas_puntuaciones(request):
    top_animes = Anime.objects.annotate(
        num_rating=Count('puntuacion')
    ).order_by('-num_rating')[:3]
    
    lista_resultados = []

    for anime_principal in top_animes:
        
        notas_principal = dict(
            Puntuacion.objects.filter(anime=anime_principal)
            .values_list('idUsuario', 'puntuacion')
        )
        
        ranking_similitud = []
        
        otros_animes = Anime.objects.exclude(pk=anime_principal.pk)
        
        for otro in otros_animes:
            notas_otro = dict(
                Puntuacion.objects.filter(anime=otro)
                .values_list('idUsuario', 'puntuacion')
            )
            
            distancia = calcular_distancia_euclidea(notas_principal, notas_otro)
            
            if distancia != float('inf'):
                ranking_similitud.append({
                    'titulo': otro.titulo,
                    'distancia': round(distancia, 2)
                })
        
        ranking_similitud.sort(key=lambda x: x['distancia'])
        top_3_parecidos = ranking_similitud[:40]
        
        lista_resultados.append({
            'titulo_principal': anime_principal.titulo,
            'votos_principales': anime_principal.num_rating,
            'similares': top_3_parecidos
        })

    return render(request, 'animes_mas_puntuados.html', {
        'lista_animes': lista_resultados, 
    })
#encoding:utf-8
from main.models import Anime, Puntuacion
import csv, pathlib

path = pathlib.Path(__file__).parent.resolve() / 'data'

def populateAnime():
    Anime.objects.all().delete()

    lista=[]
    with open(file=path / 'anime.csv', mode='r', encoding='utf-8') as f:
        lector = csv.reader(f, delimiter=';')
        next(lector)
        for anime_id, name, genre, anime_type, episodes in lector:
            lista.append(Anime(animeid=anime_id, titulo=name, generos=genre, formatoDeEmision=anime_type, numEpisodios=episodes))
    Anime.objects.bulk_create(lista)

    return len(lista)

def populatePuntuacion():
    Puntuacion.objects.all().delete()

    lista=[]
    with open(file=path / 'ratings.csv', mode='r', encoding='utf-8') as f:
        lector = csv.reader(f, delimiter=';')
        next(lector)
        for user_id, anime_id, rating in lector:
            lista.append(Puntuacion(idUsuario=user_id, anime=anime_id, puntuacion=int(rating)))
    Puntuacion.objects.bulk_create(lista)

    return Puntuacion.objects.count()


def populate():
    a = populateAnime()
    p = populatePuntuacion()
    return (a, p)
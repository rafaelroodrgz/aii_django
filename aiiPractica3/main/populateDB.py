#encoding:utf-8
from main.models import Anime, Puntuacion
import csv

path = "data"

def populateAnime():
    Anime.objects.all().delete()

    lista=[]
    with open(file=path + '/anime.csv', mode='r', encoding='utf-8') as f:
        lector = csv.reader(f, delimiter=';')
        next(lector)
        for anime_id, name, genre, anime_type, episodes in lector:
            lista.append(anime_id, name, genre, anime_type, int(episodes))
    Anime.objects.bulk_create(lista)

    return len(lista)

def populatePuntuacion():
    Puntuacion.objects.all().delete()

    lista=[]
    with open(file=path + '/ratings.csv', mode='r', encoding='utf-8') as f:
        lector = csv.reader(f, delimiter=';')
        next(lector)
        for user_id, anime_id, rating in lector:
            lista.append(user_id, anime_id, int(rating))
    Puntuacion.objects.bulk_create(lista)

    return Puntuacion.objects.count()


def populate():
    a = populateAnime()
    p = populatePuntuacion()
    return (a, p)
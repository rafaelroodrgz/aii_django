from django.db import models

class Anime(models.Model):
    animeid = models.CharField(
        max_length=10, 
        primary_key=True, 
        verbose_name='ID Anime'
    )
    titulo = models.CharField(max_length=100, verbose_name='Título')
    generos = models.CharField(max_length=100, verbose_name='Géneros')
    formatoDeEmision = models.CharField(max_length=100, verbose_name='Formato de Emisión')
    numEpisodios = models.IntegerField(verbose_name='Número de Episodios')

    def __str__(self):
        return self.titulo

class Puntuacion(models.Model):
    idUsuario = models.CharField(max_length=10, verbose_name='ID Usuario')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE) 
    puntuacion = models.FloatField(verbose_name='Puntuación')
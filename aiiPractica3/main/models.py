from django.db import models

class FormatoDeEmision(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Formato de Emisión')

    def __str__(self):
        return self.nombre
    
class Anime(models.Model):
    animeid = models.CharField(
        max_length=10, 
        primary_key=True, 
        verbose_name='ID Anime'
    )
    titulo = models.CharField(max_length=100, verbose_name='Título')
    generos = models.CharField(max_length=100, verbose_name='Géneros')
    formatoDeEmision = models.ForeignKey(FormatoDeEmision, on_delete=models.CASCADE, verbose_name='Formato de Emisión')
    numEpisodios = models.CharField(max_length=10, verbose_name='Número de Episodios')

    def __str__(self):
        return self.titulo

class Puntuacion(models.Model):
    idUsuario = models.CharField(max_length=10, verbose_name='ID Usuario')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE) 
    puntuacion = models.FloatField(verbose_name='Puntuación')
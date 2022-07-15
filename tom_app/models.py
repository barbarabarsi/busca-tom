from django.db import models

# Create your models here.
class Musica(models.Model):
    nome = models.CharField(max_length=255, default="")
    tom = models.CharField(max_length=255)
    vetor = models.CharField(max_length=10000)
    url = models.CharField(max_length=255)

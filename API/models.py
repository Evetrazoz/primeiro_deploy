
from django.db import models

# Create your models here.

class Livro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    publicado_em = models.DateField()

    def __str__(self):
        return self.titulo
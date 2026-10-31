from django.db import models

# Create your models here.
class EscapeRecord(models.Model):
    animal = models.CharField(max_length=50)
    mapa = models.CharField(max_length=50)
    tempo_fuga = models.FloatField()
    data = models.DateTimeField(auto_now_add=True)
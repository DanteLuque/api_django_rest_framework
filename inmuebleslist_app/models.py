from django.db import models

class Inmueble(models.Model):
    direccion = models.CharField(max_length=250)
    pais = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=500)
    precio = models.FloatField(default=0)
    imagen = models.CharField(max_length=900)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.direccion
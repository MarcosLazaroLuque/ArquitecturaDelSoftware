from django.db import models

<<<<<<< HEAD
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Coche(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    matricula = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.matricula}"

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    coches = models.ManyToManyField(Coche, through='CocheServicio')

    def __str__(self):
        return self.nombre

class CocheServicio(models.Model):
    coche = models.ForeignKey(Coche, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
=======
# Create your models here.
>>>>>>> 41263e665ae1dcc967eb641006b9b880fd8bc7eb

from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
# Create your models here.

class Comuna(models.Model):
    nombreComuna = models.CharField(max_length=45, verbose_name='Comuna') 
    idComuna = models.CharField(primary_key=True, max_length=15, verbose_name='ID comuna')

    def __str__(self):
        return self.nombreComuna

class Direccion(models.Model):
    nombreDireccion = models.CharField(max_length=50, verbose_name='Dirección')
    codigoPostal = models.CharField(primary_key=True, max_length=50, verbose_name='Código Postal')
    Comuna = models.ForeignKey(Comuna, on_delete=models.PROTECT)

    def __str__(self):
     return self.nombreDireccion

class Producto(models.Model):
    nombreProducto = models.CharField(max_length=50, verbose_name='Nombre del Producto')
    codigoProducto = models.CharField(max_length=10, primary_key=True, verbose_name='Código')
    precio = models.IntegerField()
    descripcion = models.TextField()

    def __str__(self):
        return self.codigoProducto

class Compra(models.Model):
    codigoCompra = models.CharField(max_length=15, primary_key=True, verbose_name='Código de compra')
    fechaCompra = models.DateField()
    Producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    Direccion = models.ForeignKey(Direccion, on_delete=models.PROTECT)

    def __str__(self):
        return self.codigoCompra

class Cliente(models.Model):
    Compra = models.ForeignKey(Compra, on_delete=models.PROTECT)
    rutCliente = models.CharField(primary_key=True, max_length=11, verbose_name='Rut Cliente')
    nombreCliente = models.CharField(max_length=50, verbose_name='Nombre')
    emailCliente = models.CharField(max_length=50, verbose_name='Email')

    def __str__(self):
        return self.rutCliente








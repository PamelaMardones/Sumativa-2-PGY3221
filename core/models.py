from django.db import models

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

class Persona(models.Model):
    rut = models.CharField(max_length=11, primary_key=True, verbose_name='Rut')
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    email = models.CharField(max_length=50, verbose_name='Email')
    contraseña = models.CharField(max_length=40, verbose_name='Contraseña')

    def __str__(self):
        return self.rut

class Cliente(models.Model):
    Compra = models.ForeignKey(Compra, on_delete=models.PROTECT)
    rutCliente = models.CharField(primary_key=True, max_length=11, verbose_name='Rut Cliente')
    nombreCliente = models.CharField(max_length=50, verbose_name='Nombre')
    emailCliente = models.CharField(max_length=50, verbose_name='Email')

    def __str__(self):
        return self.rutCliente









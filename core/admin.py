from django.contrib import admin
from .models import Comuna, Direccion, Producto, Compra, Cliente

# Register your models here.

admin.site.register(Comuna)
admin.site.register(Direccion)
admin.site.register(Producto)
admin.site.register(Compra)
admin.site.register(Cliente)
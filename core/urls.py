from django.urls import path
from .views import home, actualizar,juegos_mesa,juegos,magic,pokemon,registro,yugioh


urlpatterns = [
    path('', home, name = "home"),
    path('actualizar-perfil/', actualizar, name = "actualizar_perfil"),
    path('juegos-mesa/', juegos_mesa, name = "juegos_mesa"),
    path('juegos/', juegos, name = "juegos"),
    path('magic/', magic, name = "magic"),
    path('pokemon/', pokemon, name = "pokemon"),
    path('registro/', registro, name = "registro"),
    path('yugioh/', yugioh, name = "yugioh"),
]
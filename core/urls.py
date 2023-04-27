from django.urls import path
from .views import home, actualizar,juegos_mesa, login_view,magic,pokemon,register,yugioh, logout_view, update


urlpatterns = [
    path('', home, name = "home"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('actualizar-perfil/', actualizar, name = "actualizar_perfil"),
    path('actualizar/', update, name = "actualizar"),
    path('juegos-mesa/', juegos_mesa, name = "juegos_mesa"),
    path('magic/', magic, name = "magic"),
    path('pokemon/', pokemon, name = "pokemon"),
    path('registro/', register, name = "registro"),
    path('yugioh/', yugioh, name = "yugioh"),
]
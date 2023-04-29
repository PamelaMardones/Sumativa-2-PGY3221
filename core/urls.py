from django.urls import path
from .views import add_to_cart, cart, checkout, home, actualizar,juegos_mesa, login_view,magic,pokemon,register, remove_from_cart,yugioh, logout_view, update, search


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
    path('search/', search, name = "search"),
    path('cart/<int:cart_id>/', cart, name = "cart"),
    path('add-to-cart/<int:cart_id>/<int:product_id>/', add_to_cart, name = "add_to_cart"),
    path('remove-from-cart/<int:cart_id>/<int:product_id>/', remove_from_cart, name = "remove_from_cart"),
    path('checkout/<int:cart_id>/', checkout, name = "checkout")
]
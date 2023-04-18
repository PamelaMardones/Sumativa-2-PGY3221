from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'core/home.html')

@method_decorator(login_required, name='dispatch')
class actualizar(View):
    def get(self, request):
        return render(request, 'core/actualizar-perfil.html')

def juegos_mesa(request):
    return render(request, 'core/juegos-mesa.html')

def juegos(request):
    return render(request, 'core/juegos.html')

def magic(request):
    return render(request, 'core/magic.html')

def pokemon(request):
    return render(request, 'core/pokemon.html')

def registro(request):
    return render(request, 'core/registro.html')

def yugioh(request):
    return render(request, 'core/yugioh.html')
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

# Create your views here.


def home(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        persona = authenticate(request, username=email, password=password)
        if persona is not None:
            login(request, persona)
            return redirect('home')  # <-- reemplace con la página de inicio deseada
        else:
            mensaje = 'Credenciales inválidas'
    else:
        mensaje = ''
        print("mipico")

    return render(request, 'dashboard/home.html')

def actualizar(request):
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

def logout_view(request):
    logout(request)
    del request.session['user'] # Eliminamos la variable user de la sesión
    return redirect('home') # Redirigimos al usuario a la página de inicio de la aplicación
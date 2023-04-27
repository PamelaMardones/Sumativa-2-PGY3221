from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
import requests

def home(request):
    return render(request, 'dashboard/home.html')

def actualizar(request):
    if not request.user.is_authenticated:
        return redirect('home')
    return render(request, 'core/actualizar-perfil.html')

def juegos_mesa(request):
    return render(request, 'core/juegos-mesa.html')

def magic(request):
    return render(request, 'core/magic.html')

def pokemon(request):
    return render(request, 'core/pokemon.html')

def registro(request):
    return render(request, 'core/registro.html')

def yugioh(request):
    #get products from API
    api_response = requests.get('https://duocucpgy3221api-production.up.railway.app/api/products/')
    
    if api_response.status_code not in [200, 201]:
        return redirect('home')
    
    #filter products by type=0 and catergory=2
    products = [product for product in api_response.json() if product['type'] == 2 and product['category'] == 0] 
    
    print(products)
        

    return render(request, 'core/yugioh.html', {'products': products})

def logout_view(request):
    logout(request)
    return render(request, 'dashboard/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Mostrar mensaje de error de inicio de sesión
            error_message = 'Nombre de usuario o contraseña incorrectos.'
            return render(request, 'dashboard/home.html', {'error_message': error_message})
    else:
        return render(request, 'dashboard/home.html')
    
def register(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Validar que las contraseñas coincidan
        if password == password2:
            # Crear el usuario
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Autenticar al usuario y redirigir a la página de inicio
            auth_user = authenticate(username=username, password=password)
            login(request, auth_user)

            # save the user on API
            api_response = requests.post('https://duocucpgy3221api-production.up.railway.app/api/users/', data={
                'id': user.id,
                'username': user.username,
            })

            if api_response.status_code not in [200, 201]:
                return render(request, 'core/registro.html', {'error': 'No se pudo registrar el usuario.'})

            return redirect('home')
        else:
            # Mostrar un error si las contraseñas no coinciden
            error_msg = "Las contraseñas no coinciden."
            return render(request, 'core/registro.html', {'error': error_msg})
    else:
        return render(request, 'core/registro.html')
    
def update(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user = request.user
        usuario = User.objects.get(username=user.username)


        usuario.first_name = first_name
        usuario.last_name = last_name
        usuario.email = email
        usuario.save()

        # Redirigir a la página de inicio
        return redirect('home')
    else:
        return render(request, 'core/home.html')
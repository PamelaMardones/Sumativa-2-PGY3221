from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
import requests

def home(request):
    #get orders_items from API. Last 5 order_items
    api_response = requests.get('https://duocucpgy3221api-production.up.railway.app/api/order_items/last_five/')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        return render(request, 'dashboard/home.html', {'error': 'No se pudo obtener los productos.'})

    #get products from API filter by product_id in orders_items
    products = [requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/products/{order_item["product"]}/').json() for order_item in api_response.json()]

    #if the user is not authenticated, render the template with the products
    if not request.user.is_authenticated:
        return render(request, 'dashboard/home.html', {'products': products})

    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/cart/get_cart/?user={request.user.id}')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        api_response = requests.post('https://duocucpgy3221api-production.up.railway.app/api/cart/create_cart/', json={'user': request.user.id})

        #check if the response is ok
        if api_response.status_code not in [200, 201]:
            #redirect to home and send alert
            return render(request, 'dashboard/home.html', {'error': 'No se pudo crear el carrito.', 'products': products})

        print(api_response.json())
        #get cart from API
        api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/cart/get_cart/?user={request.user.id}')

        print(api_response.json())
        #check if the response is ok
        if api_response.status_code not in [200, 201]:
            #redirect to home and send alert
            return render(request, 'dashboard/home.html', {'error': 'No se pudo obtener el carrito.', 'products': products})
        
    cart = api_response.json()

    return render(request, 'dashboard/home.html', {'products': products, 'cart': cart})

def actualizar(request):
    if not request.user.is_authenticated:
        return redirect('home')
    return render(request, 'core/actualizar-perfil.html')

def juegos_mesa(request):
    #get products from API
    api_response = requests.get('https://duocucpgy3221api-production.up.railway.app/api/products/')

    #check if the response is ok    
    if api_response.status_code not in [200, 201]:
        return redirect('home')
    
    #filter products by type=3 and catergory=1
    products = [product for product in api_response.json() if product['type'] == 3 and product['category'] == 1] 

    return render(request, 'core/juegos-mesa.html', {'products': products})

def magic(request):
    api_response = requests.get('https://duocucpgy3221api-production.up.railway.app/api/products/')

    if api_response.status_code not in [200, 201]:
        return redirect('home')

    products = [product for product in api_response.json() if product['type'] == 1 and product['category'] == 0] 
    return render(request, 'core/magic.html', {'products': products})

def pokemon(request):
    return render(request, 'core/pokemon.html')

def registro(request):
    return render(request, 'core/registro.html')

def yugioh(request):
    #get products from API
    api_response = requests.get('https://duocucpgy3221api-production.up.railway.app/api/products/')

    #check if the response is ok    
    if api_response.status_code not in [200, 201]:
        return redirect('home')
    
    #filter products by type=0 and catergory=2
    products = [product for product in api_response.json() if product['type'] == 2 and product['category'] == 0] 

    #render the template with the products
    return render(request, 'core/yugioh.html', {'products': products})

def logout_view(request):
    logout(request)

    #get orders_items from API. Last 5 order_items
    api_response = requests.get('https://duocucpgy3221api-production.up.railway.app/api/order_items/last_five/')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        return render(request, 'dashboard/home.html', {'error': 'No se pudo obtener los productos.'})

    #get products from API filter by product_id in orders_items
    products = [requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/products/{order_item["product"]}/').json() for order_item in api_response.json()]

    return render(request, 'dashboard/home.html', {'products': products})

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
        return redirect('home')
    
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
                # delete the user if the API request fails
                user.delete()
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
        return redirect('home')
    
def cart(request, cart_id):
    #get cart from API
    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/cart/get_cart/?user={request.user.id}')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        #redirect to home and send alert
        return redirect('home', {'error': 'No se pudo obtener el carrito.'})
    
    cart = api_response.json()

    return render(request, 'core/cart.html', {'cart': cart})

def add_to_cart(request, cart_id, product_id):
    #get cart from API
    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/cart/{cart_id}/')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        #redirect to home and send alert
        return redirect('home', {'error': 'No se pudo obtener el carrito.'})
    
    cart = api_response.json()

    #if cart is_checked_out, redirect to home and send alert
    if cart['is_checked_out']:
        return redirect('home', {'error': 'No se pudo agregar el producto.'})
    
    #get product from API
    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/products/{product_id}/')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        #redirect to home and send alert
        return redirect('home', {'error': 'No se pudo obtener el producto.'})
    
    product = api_response.json()

    #add product to cart
    api_response = requests.post(f'https://duocucpgy3221api-production.up.railway.app/api/cart/{cart_id}/add_to_cart/', data={
        'product': product_id,
        'qty': 1
    })

    print(api_response.json())

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        #redirect to home and send alert
        return redirect('home', {'error': 'No se pudo agregar el producto.'})
    
    #return to same page
    return redirect('cart', cart_id=cart_id)

def remove_from_cart(request, cart_id, product_id):
    #get cart where is_checked_out=False for his user
    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/cart/get_cart/?user={request.user.id}')


    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        #redirect to home and send alert
        return render(request, 'core/cart.html', {'error': 'No se pudo obtener el carrito.'})
    
    cart = api_response.json()

    #if cart is_checked_out, redirect to home and send alert
    if cart['is_checked_out']:
        return render(request, 'core/cart.html', {'cart': cart, 'error': 'No se pudo eliminar el producto.'})

    #get product from API
    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/products/{product_id}/')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        #redirect to home and send alert
        return render(request, 'core/cart.html', {'cart': cart, 'error': 'No se pudo obtener el producto.'})

    #remove product from cart in API (product send in json)
    api_response = requests.delete(f'https://duocucpgy3221api-production.up.railway.app/api/cart/{cart_id}/remove_from_cart/', data={
        'product': product_id
    })
    
    print(api_response.json())

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        #redirect to home and send alert
        return render(request, 'core/cart.html', {'cart': cart, 'error': 'No se pudo eliminar el producto.'})

    return redirect('cart', cart_id=cart_id)

def checkout(request, cart_id):
    #get cart from API
    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/cart/{cart_id}/')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        #redirect to home and send alert
        return redirect('home', {'error': 'No se pudo obtener el carrito.'})
    
    cart = api_response.json()

    #if cart is_checked_out, redirect to home and send alert
    if cart['is_checked_out']:
        return render(request, 'core/cart.html', {'cart': cart, 'error': 'El carrito ya fue pagado.'})
    
    #update cart in API
    api_response = requests.post(f'https://duocucpgy3221api-production.up.railway.app/api/cart/{cart_id}/checked_out/')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        #redirect to home and send alert
        return redirect('cart', cart_id=cart_id)
    
    return redirect('home')

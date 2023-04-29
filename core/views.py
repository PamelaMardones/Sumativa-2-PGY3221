from os import replace
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
import requests

def get_cart(request):
    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/cart/get_cart/?user={request.user.id}')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        api_response = requests.post('https://duocucpgy3221api-production.up.railway.app/api/cart/create_cart/', json={'user': request.user.id})

        #check if the response is ok
        if api_response.status_code not in [200, 201]:
            messages.add_message(request, messages.ERROR, 'No se pudo crear el carrito.')
            return redirect('home')

        #get cart from API
        api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/cart/get_cart/?user={request.user.id}')

        #check if the response is ok
        if api_response.status_code not in [200, 201]:
            messages.add_message(request, messages.ERROR, 'No se pudo obtener el carrito.')
            return redirect('home')
        
    cart = api_response.json()

    return cart

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
        
    cart = get_cart(request)

    return render(request, 'dashboard/home.html', {'products': products, 'cart': cart})

def actualizar(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Debes iniciar sesión para actualizar tu perfil.')
        return redirect('home')
    
    cart = get_cart(request)

    return render(request, 'core/actualizar-perfil.html', {'cart': cart})

def juegos_mesa(request):
    #get products from API
    api_response = requests.get('https://duocucpgy3221api-production.up.railway.app/api/products/')

    #check if the response is ok    
    if api_response.status_code not in [200, 201]:
        messages.add_message(request, messages.ERROR, 'No se pudo obtener los productos.')
        return redirect('home')
    
    #filter products by type=3 and catergory=1
    products = [product for product in api_response.json() if product['type'] == 3 and product['category'] == 1] 

    if not request.user.is_authenticated:
        return render(request, 'core/juegos-mesa.html', {'products': products})
    
    cart = get_cart(request)

    return render(request, 'core/juegos-mesa.html', {'products': products, 'cart': cart})

def magic(request):
    api_response = requests.get('https://duocucpgy3221api-production.up.railway.app/api/products/')

    if api_response.status_code not in [200, 201]:
        messages.add_message(request, messages.ERROR, 'No se pudo obtener los productos.')
        return redirect('home')

    products = [product for product in api_response.json() if product['type'] == 1 and product['category'] == 0] 

    if not request.user.is_authenticated:
        return render(request, 'core/magic.html', {'products': products})
    
    cart = get_cart(request)

    return render(request, 'core/magic.html', {'products': products, 'cart': cart})

def pokemon(request):
    #get products from API
    api_response = requests.get('https://duocucpgy3221api-production.up.railway.app/api/products/')
    #check if the response is ok    
    if api_response.status_code not in [200, 201]:
        return redirect('home')
    
    #filter products by type=0 and catergory=2
    products = [product for product in api_response.json() if product['type'] == 0 and product['category'] == 0] 

    if not request.user.is_authenticated:
        return render(request, 'core/pokemon.html', {'products': products})
    
    cart = get_cart(request)

    #render the template with the products
    return render(request, 'core/pokemon.html', {'products': products, 'cart': cart})

def registro(request):
    return render(request, 'core/registro.html')

def yugioh(request):
    #get products from API
    api_response = requests.get('https://duocucpgy3221api-production.up.railway.app/api/products/')

    #check if the response is ok    
    if api_response.status_code not in [200, 201]:
        messages.add_message(request, messages.ERROR, 'No se pudo obtener los productos.')
        return redirect('home')
    
    #filter products by type=0 and catergory=2
    products = [product for product in api_response.json() if product['type'] == 2 and product['category'] == 0] 

    if not request.user.is_authenticated:
        return render(request, 'core/yugioh.html', {'products': products})
    
    cart = get_cart(request)

    #render the template with the products
    return render(request, 'core/yugioh.html', {'products': products, 'cart': cart})

def logout_view(request):
    logout(request)

    #get orders_items from API. Last 5 order_items
    api_response = requests.get('https://duocucpgy3221api-production.up.railway.app/api/order_items/last_five/')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        messages.add_message(request, messages.ERROR, 'No se pudo obtener los productos.')
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
            messages.add_message(request, messages.INFO, 'Usuario o contraseña incorrectos.')
            return render(request, 'dashboard/home.html')
    else:
        messages.add_message(request, messages.INFO, 'Error al iniciar sesión.')
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
                messages.add_message(request, messages.ERROR, 'No se pudo registrar el usuario.')
                user.delete()
                return render(request, 'core/registro.html')

            messages.add_message(request, messages.SUCCESS, 'Usuario registrado correctamente.')
            return redirect('home')
        else:
            # Mostrar un error si las contraseñas no coinciden
            messages.add_message(request, messages.ERROR, 'Las contraseñas no coinciden.')
            return render(request, 'core/registro.html')
    else:
        messages.add_message(request, messages.ERROR, 'No se pudo registrar el usuario.')
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

        messages.add_message(request, messages.SUCCESS, 'Datos actualizados correctamente.')
        return redirect('home')
    else:
        return redirect('home')
    
def cart(request, cart_id):
    #get cart from API
    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/cart/get_cart/?user={request.user.id}')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        messages.add_message(request, messages.ERROR, 'No se pudo obtener el carrito.')
        #redirect to home and send alert
        return redirect('home')
    
    cart = api_response.json()

    return render(request, 'core/cart.html', {'cart': cart})

def add_to_cart(request, cart_id, product_id):
    #get qty from request
    qty = request.POST.get('qty')

    if not qty:
        qty = 1

    #get cart from API
    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/cart/{cart_id}/')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        messages.add_message(request, messages.ERROR, 'No se pudo obtener el carrito.')
        #redirect to home and send alert
        return redirect('home')
    
    cart = api_response.json()

    #if cart is_checked_out, redirect to home and send alert
    if cart['is_checked_out']:
        messages.add_message(request, messages.ERROR, 'No se pudo agregar el producto.')
        return redirect('home')
    
    #get product from API
    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/products/{product_id}/')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        messages.add_message(request, messages.ERROR, 'No se pudo obtener el producto.')
        #redirect to home and send alert
        return redirect('home')

    #add product to cart
    api_response = requests.post(f'https://duocucpgy3221api-production.up.railway.app/api/cart/{cart_id}/add_to_cart/', data={
        'product': product_id,
        'qty': qty
    })

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        messages.add_message(request, messages.ERROR, 'No se pudo agregar el producto.')
        #redirect to home and send alert
        return redirect('home')
    
    messages.add_message(request, messages.SUCCESS, 'Producto agregado correctamente.')
    return redirect('cart', cart_id=cart_id)

def remove_from_cart(request, cart_id, product_id):
    #get cart where is_checked_out=False for his user
    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/cart/get_cart/?user={request.user.id}')


    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        messages.add_message(request, messages.ERROR, 'No se pudo obtener el carrito.')
        #redirect to home and send alert
        return render(request, 'core/cart.html')
    
    cart = api_response.json()

    #if cart is_checked_out, redirect to home and send alert
    if cart['is_checked_out']:
        messages.add_message(request, messages.ERROR, 'Este carrito ya fue pagado.')
        return render(request, 'core/cart.html', {'cart': cart})

    #get product from API
    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/products/{product_id}/')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        #redirect to home and send alert
        messages.add_message(request, messages.ERROR, 'No se pudo obtener el producto.')
        return render(request, 'core/cart.html', {'cart': cart})

    #remove product from cart in API (product send in json)
    api_response = requests.delete(f'https://duocucpgy3221api-production.up.railway.app/api/cart/{cart_id}/remove_from_cart/', data={
        'product': product_id
    })

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        messages.add_message(request, messages.ERROR, 'No se pudo eliminar el producto.')
        #redirect to home and send alert
        return render(request, 'core/cart.html', {'cart': cart})

    messages.add_message(request, messages.SUCCESS, 'Producto eliminado del carrito.')
    return redirect('cart', cart_id=cart_id)

def checkout(request, cart_id):
    #get cart from API
    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/cart/{cart_id}/')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        messages.add_message(request, messages.ERROR, 'No se pudo realizar la compra.')
        #redirect to home and send alert
        return redirect('home')
    
    cart = api_response.json()

    #if cart is_checked_out, redirect to home and send alert
    if cart['is_checked_out']:
        messages.add_message(request, messages.ERROR, 'Este carrito ya fue pagado.')
        return render(request, 'core/cart.html', {'cart': cart})
    
    #update cart in API
    api_response = requests.post(f'https://duocucpgy3221api-production.up.railway.app/api/cart/{cart_id}/checked_out/')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        messages.add_message(request, messages.ERROR, 'No se pudo realizar la compra.')
        return redirect('cart', cart_id=cart_id)
    
    messages.add_message(request, messages.SUCCESS, 'Compra realizada con éxito.')
    return redirect('home')

def search(request):
    #get search term from form
    search_term = request.POST.get('search_term', '')

    #get products with search term like %% from API
    api_response = requests.get(f'https://duocucpgy3221api-production.up.railway.app/api/products/search/?name={search_term}')

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        messages.add_message(request, messages.ERROR, 'No se encontraron productos.')
        #redirect to home and send alert
        return redirect('home')
    
    products = api_response.json()

    if not request.user.is_authenticated:
        return render(request, 'core/search.html', {'products': products, 'search_term': search_term})
    
    cart = get_cart(request)

    return render(request, 'core/search.html', {'products': products, 'search_term': search_term, 'cart': cart})

def pokedex(request):
    page_number = request.GET.get('page_number', 0)
    limit = request.GET.get('limit', 12)
    offset = request.GET.get('offset', 0)

    page_number = int(page_number)
    limit = int(limit)
    offset = int(offset.replace(',', ''))

    current_page = f'https://pokeapi.co/api/v2/pokemon/?limit={limit}&offset={offset}'

    #get pokemons from API
    api_response = requests.get(current_page)

    #check if the response is ok
    if api_response.status_code not in [200, 201]:
        messages.add_message(request, messages.ERROR, 'No se encontraron pokemones.')
        #redirect to home and send alert
        return redirect('home')
    
    pokemon_list = api_response.json()

    for pokemon in pokemon_list['results']:
        api_response = requests.get(pokemon['url'])

        result = api_response.json()

        pokemon['id'] = result['id']
        pokemon['abilities'] = result['abilities']
        pokemon['height'] = result['height']
        pokemon['weight'] = result['weight']
        pokemon['types'] = result['types']
        pokemon['image'] = result['sprites']['front_default']
        pokemon['types'] = result['types']
        pokemon['stats'] = result['stats']

    total_pages = int(pokemon_list['count']) / limit
    total_pages = int(total_pages)

    pages_info = []
    x = 1
    #for 10 pages from current page to total pages
    for i in range(page_number, page_number + 10):
        if page_number + x <= total_pages:
            print(i)
            next_page = {}
            next_page['page_number'] = page_number + x
            next_page['limit'] = limit
            next_page['offset'] = offset + (limit * x)
            pages_info.append(next_page)
        x += 1
        print('x' + str(x))

    pokemon_list['pagination'] = {
        'final_page': total_pages,
        'final_offset': int(total_pages * limit),
        'current_page': page_number,
        'previous_page': page_number - 1,
        'previous_offset': offset - limit,
        'next_page': page_number + 1,
        'next_offset': offset + limit,
        'next_pages': pages_info
    }

    if not request.user.is_authenticated:
        return render(request, 'core/pokedex.html', {'pokemon_list': pokemon_list, 'page_number': page_number})
    
    cart = get_cart(request)

    return render(request, 'core/pokedex.html', {'pokemon_list': pokemon_list, 'cart': cart})
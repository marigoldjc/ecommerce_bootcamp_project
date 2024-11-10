from django.shortcuts import render, redirect
from .forms import CheckoutForm
from .models import *
from django.http import HttpResponse
import uuid

# Homepage View
def homepage(request):
    categories = Category.objects.all()
    return render(request, 'ecommerce_app/homepage.html', {'categories': categories})

# Product Page View
def product_page(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'ecommerce_app/product_page.html', {'product': product})

# Cart Page View
def cart_page(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + 1  # Increment quantity
        request.session['cart'] = cart
        return redirect('cart_page')
    
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    return render(request, 'ecommerce_app/cart_page.html', {'cart': cart, 'products': products})

def cart(request):
    items = cart.cartitem_set.all()
    items = []
    cart = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items, 'order':order}
    return render(request, 'ecommerce_app/cart_page.html, context)

def checkout_page(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Generate a unique confirmation number
            confirmation_number = str(uuid.uuid4())  # Generate a unique UUID

            # Process the order here (e.g., save to the database)
            # You can also store the confirmation number in the database if needed

            # Clear the cart after the order is placed
            request.session['cart'] = {}

            # Prepare the confirmation page context
            cart_items = request.session.get('cart', {})
            cart_summary = []
            for product_id, quantity in cart_items.items():
                product = Product.objects.get(id=product_id)  # Fetch product details
                cart_summary.append({
                    'product_name': product.name,
                    'quantity': quantity,
                    'price': product.price
                })

            return render(request, 'ecommerce_app/confirmation_page.html', {
                'cart': {'items': cart_summary},
                'confirmation_number': confirmation_number
            })
    else:
        form = CheckoutForm()

    # Fetch products for the cart display
    cart_items = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart_items.keys())  # Get products in cart

    return render(request, 'ecommerce_app/checkout_page.html', {
        'form': form,
        'cart': {'items': cart_items},
        'products': products
    })
    
# Confirmation Page View
def confirmation_page(request):
    return render(request, 'ecommerce_app/confirmation_page.html')

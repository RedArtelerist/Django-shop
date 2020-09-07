from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import *

# Create your views here.


def index(request):

    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    return render(request, 'main/index.html', {'title': 'Main page', 'cartItems': cartItems})


def about(request):

    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    return render(request, 'main/about.html', {'cartItems': cartItems})


def store(request):

    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    categories = Category.objects.order_by('name')
    products = Product.objects.filter(isActive=True)

    return render(request, 'main/store.html', {'title': 'Store', 'products': products, 'categories': categories, 'cartItems': cartItems})


def product(request, product_id):

    cookieData = cartData(request)
    cartItems = cookieData['cartItems']

    product = Product.objects.get(id=product_id)
    return render(request, 'main/product.html', {'title': product.name, 'product': product, 'cartItems': cartItems})


def cart(request):

    cookieData = cartData(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']

    return render(request, 'main/cart.html', {'title': 'Cart', 'items': items, 'order': order, 'cartItems': cartItems})


def checkout(request):

    cookieData = cartData(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']

    return render(request, 'main/checkout.html', {'title': 'Checkout', 'items': items, 'order': order, 'cartItems': cartItems})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action', action)
    print('productId', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.delete()
        return JsonResponse('Item was added', safe=False)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        print(order.shipping)

    else:
        customer, order = guestData(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        print('Shipping address')
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            country=data['shipping']['country'],
            state=data['shipping']['state'],
            city=data['shipping']['city'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete!', safe=False)

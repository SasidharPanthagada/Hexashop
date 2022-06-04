from unicodedata import category
from django.shortcuts import render
from .models import *
import json
import datetime
from django.http import JsonResponse
from django.core.paginator import Paginator , EmptyPage
# Create your views here.

def index(request):

    products = Product.objects.all
    

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer , complete = False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else :
        items=[]
        order = {'get_cart_items':0,}
        cart_items = order['get_cart_items']

    data = {'items':items,'order':order,'products':products,'cart_items':cart_items}
    return render(request,'index.html',data)

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def products(request,category_slug):
    if category_slug == 'all':
        products = Product.objects.all
    else :
        products = Product.objects.filter(category=category_slug)

    p = Paginator(products,2)
    page = request.GET.get('page')
    #pages = p.get_page(page)

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer , complete = False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else :
        items=[]
        order = {'get_cart_items':0,}
        cart_items = order['get_cart_items']

    data = {'items':items,'order':order,'products':products,'cart_items':cart_items,}
    return render(request,'products.html',data)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer , complete = False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else :
        items=[]
        order = {'get_cart_items':0,}
        cart_items = order['get_cart_items']

    data = {'items':items,'order':order,'cart_items':cart_items}

    return render(request , 'cart.html',data)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer , complete = False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else :
        items=[]
        order = {'get_cart_items':0,}
        cart_items = order['get_cart_items']

    data = {'items':items,'order':order,'cart_items':cart_items}

    return render(request,'checkout.html' , data)

def singleproduct(request,product_slug):
    selected_product = Product.objects.get(slug=product_slug)
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer , complete = False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else :
        items=[]
        order = {'get_cart_items':0,}
        cart_items = order['get_cart_items']

    data = {'items':items,'order':order,'products':products,'cart_items':cart_items}

    return render(request,'single-product.html',{
        'product_found': True,
        'product': selected_product,
        'cart_items':cart_items,
    })

def updateitem(request):
    data = json.loads(request.body)
    productid = data['productid']
    action = data['action']

    print('action:',action)
    print('productid:',productid)

    customer = request.user.customer
    product = Product.objects.get(id=productid)
    order , created = Order.objects.get_or_create(customer=customer , complete = False)

    orderitem , created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)

    orderitem.save()

    if orderitem.quantity <= 0 :
        orderitem.delete()

    return JsonResponse ('Item is added',safe=False)

def processorder(request):
    transactionid = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer=customer , complete = False)
        total = float(data['form']['total'])
        order.transaction_id = transactionid

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer = customer,
            order=order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    else :
        print('User is not logged in ...')
    return JsonResponse ('payment complete',safe=False)
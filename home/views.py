from ast import Pass
from aiohttp import request
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import  redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from .models import Product, Cart


def index(request):
    cart = Cart.objects.filter(userId = request.user.id)
    cartlength = len(cart)
    if request.method == "POST":
        if 'login_btn' in request.POST:
            username = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                messages.warning(request, "Email or Password is not correct.")
            return redirect('/')
        if 'register_btn' in request.POST:
            print('Clicked Register')
            form = NewUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
    form = NewUserForm()
    return render(request=request, template_name="home/index.html", context={"register_form": form, 'cartlength': cartlength})

# @login_required(login_url='/')
def productView(request):
    cart = Cart.objects.filter(userId = request.user.id)
    cartlength = len(cart)
    products = Product.objects.all()
    return render(request, 'home/products.html', context={"products": products, "cartlength": cartlength})


def logout_view(request):
    logout(request)
    return redirect('/')

def deleteCartItem(request, cid):
    if request.method == 'GET':
        Cart.objects.filter(id = int(cid)).delete()
        return redirect('/cart')
    return HttpResponse(f'{cid}')






@login_required(login_url='/')
def CartView(request):
    cart = Cart.objects.filter(userId = request.user.id)
    cartlength = len(cart)
    totalAmount = 0;
    for i in cart:
        singleItemPrize= int(i.qty)*int(i.productPrize)
        totalAmount+=singleItemPrize
    return render(request, 'home/cart.html', {'cart': cart, 'cartlength': cartlength, 'totalAmount': totalAmount})
    

@login_required(login_url='/')
def addToCart(request, pid):
    if request.user.id:
        product = Product.objects.filter(id = pid)
        carts = Cart.objects.filter( productId = pid)
        if len(carts) > 0:
            messages.error(request, 'Prouct already Added to the cart.')
            return redirect('/products')
        cart = Cart()
        cart.productId = product[0].id
        cart.productName = product[0].productName
        cart.productPrize = product[0].productPrize
        cart.productImage = product[0].productImage
        cart.userId = request.user.id
        cart.userName = request.user.first_name
        cart.userEmail = request.user.email
        cart.qty = 1
        cart.save()
    else:
        return redirect('/products')
    return HttpResponseRedirect('/cart')




def updateQty(request):
    if request.method == 'POST':
        qty = request.POST.get('qty')
        cid = request.POST.get('cid')
        uid = request.POST.get('userId')
        cartItem = Cart.objects.get(id = int(cid))
        if cartItem:
            cartItem.qty = qty
            cartItem.save()
    return HttpResponse(f'{cartItem}')
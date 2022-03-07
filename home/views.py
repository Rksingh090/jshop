from ast import Pass
import re
from urllib import request
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import  redirect, render
from django.contrib.auth import get_user
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.forms import NewUserForm, ContactForm
from django.contrib.auth import login, logout, authenticate
from .models import Orders, Product, Cart
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from home import checksum
import json

# home page - index ('/')
def index(request):
    cart = Cart.objects.filter(userId = request.user.id)
    cartlength = len(cart)
    return render(request=request, template_name="home/index.html", context={'cartlength': cartlength})

# product page - '/product'
def productView(request):
    cart = Cart.objects.filter(userId = request.user.id)
    cartlength = len(cart)
    products = Product.objects.all()
    return render(request, 'home/products.html', context={"products": products, "cartlength": cartlength})

# login and register page handler view '/login'
def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        if 'login_btn' in request.POST:
            username = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.warning(request, "Email or Password is not correct.")
        if 'register_btn' in request.POST:
            form = NewUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f"New Account Created: {username}")
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("/")
            else:
                for msg in form.error_messages:
                    messages.error(request, f"{msg}: {form.error_messages[msg]}")
                    messages.info(request, f"Choose a strong password with at least 1 Capital, 1 small, 1 Special character and at least 1 number. Minimum 8 character password.")
                    print(msg)  
    form = NewUserForm()
    return render(request, "home/Login.html",context={"register_form": form,})

# logout view 
def logout_view(request):
    logout(request)
    return redirect('/')

#delete items from cart
def deleteCartItem(request, cid):
    if request.method == 'GET':
        Cart.objects.filter(id = int(cid)).delete()
        return redirect('/cart')
    return HttpResponse(f'{cid}')

# user cart page 
@login_required(login_url='/login')
def CartView(request):
    cart = Cart.objects.filter(userId = request.user.id)
    cartlength = len(cart)
    totalAmount = 0;
    for i in cart:
        singleItemPrize= int(i.qty)*int(i.productPrize)
        totalAmount+=singleItemPrize
    return render(request, 'home/cart.html', {'cart': cart, 'cartlength': cartlength, 'totalAmount': totalAmount})
    
# add items to cart 
@login_required(login_url='/login')
def addToCart(request, pid):
    if request.user.id:
        product = Product.objects.filter(id = pid)
        carts = Cart.objects.filter( productId = pid).filter(userId = request.user.id)
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
    # else:
    #     return redirect('/products')
    return HttpResponseRedirect('/products')

# update the quantity of cart 
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

# handler checkout and redirect to payment method '/checkout'
def CheckoutView(request):
    cart = Cart.objects.filter(userId=request.user.id)
    cartlength = len(cart)
    if request.method == 'POST':
        itemJson = request.POST.get('itemJson')
        totalAmount = request.POST.get('totalAmount')
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('pinCode')
        phone = request.POST.get('phone')

        # save order into database 
        order = Orders(order_json=itemJson, userId=request.user.id, userName=name, userEmail=email, userAddress=address, city=city, state=state,zip_code=zip_code, phone=phone, totalAmount=int(totalAmount))
        order.save()
        toFixCart = Cart.objects.filter(userId=request.user.id)
        oid = str('OIDNO'+str(order.orderId))
        # if len(toFixCart) > 1:
        for i in toFixCart:
            i.orderId = int(order.orderId)
            i.save()

        # generating dictionary to generate hash and pass to paytm 
        param_dict = {
            'MID': 'AXngIz82728101827788',
            'ORDER_ID': oid,
            'TXN_AMOUNT': str(order.totalAmount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	    'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest',
        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, "H#IFitj!PqI6T1wA")
        return render(request, 'home/paytm.html', {"param_dict": param_dict})

    checkout = Cart.objects.filter(userId=request.user.id)
    if len(checkout) <= 0:
        return redirect('/cart')
    totalAmount = 0   
    jsonData = serializers.serialize('json', queryset=checkout)
    for items in checkout:
        totalAmount += int(items.productPrize)*int(items.qty)
    return render(request, 'home/Checkout.html', {"checkout": checkout, "totalPrize": totalAmount, 'jsonData': jsonData, "cartlength": cartlength})

# handle the response from the paytm after payment 'handlerequest'
@csrf_exempt
def handleRequest(request):
    
    if request.method == 'POST':
        form = request.POST
        response_dict = {}
        rschecksum = ''

        for i in form.keys():
            response_dict[i] = form[i]
            if i == "CHECKSUMHASH":
                rschecksum = form[i]
        verify = checksum.verify_checksum(response_dict,merchant_key="H#IFitj!PqI6T1wA",checksum=rschecksum)

        if verify:
            if response_dict['RESPCODE'] == '01':
                print("order")
                oid = response_dict['ORDERID']
                pOrder = Orders.objects.get(orderId = int(oid[5:]))
                pOrder.paymentStatus = 'DONE'
                pOrder.save()
                Cart.objects.filter(orderId=int(oid[5:])).delete()
            else:
                oid = response_dict['ORDERID']
                Orders.objects.filter(orderId=int(oid[5:])).delete()

        return render(request, 'home/paymentstatus.html', {"response": response_dict})

# searching product items 
def SearchView(request):
    cart = Cart.objects.filter(userId=request.user.id)
    cartlength = len(cart)
    data = request.GET.get('q')
    products = Product.objects.filter(productName__contains=data)
    return render(request, 'home/products.html', context={"products": products, "cartlength": cartlength, "isSearchPage": True, "searchTerm": data})

# about page '/about'
def aboutView(request):
    return render(request, "pages/about.html")

# contact page '/contact'
def contactView(request):
    cForm = ContactForm()
    if request.method == "POST":
        contactF = ContactForm(request.POST)
        if contactF.is_valid():
            contactF.save()
            messages.success(request,"You message reached to us. We will connect with you in a moment.")
            return redirect('/')
        else:
            messages.info(request,"Please enter correct email !")

    return render(request, "pages/contact.html", context={"contact_form": cForm})
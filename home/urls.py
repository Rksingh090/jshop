from django.urls import path
from django.conf import global_settings as settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.loginView, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('products', views.productView, name='products'),
    path('cart', views.CartView, name='cart'),
    path('addtocart/<pid>', views.addToCart, name='add_to_cart'),
    path('updateqty', views.updateQty, name='updateqty'),
    path('deletecartitem/<cid>', views.deleteCartItem, name='deletecartitem'),
    path('checkout', views.CheckoutView, name='checkout'),
    path('search', views.SearchView, name='search'),
    path('handlerequest', views.handleRequest, name='handlerequest'),
    path('about', views.aboutView, name='about'),
    path('contact', views.contactView, name='contact'),
] 



from django.urls import path
from django.conf import global_settings as settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('logout', views.logout_view, name='logout'),
    path('products', views.productView, name='products'),
    path('cart', views.CartView, name='cart'),
    path('addtocart/<pid>', views.addToCart, name='add_to_cart'),
    path('updateqty', views.updateQty, name='updateqty'),
    path('deletecartitem/<cid>', views.deleteCartItem, name='deletecartitem'),
] 



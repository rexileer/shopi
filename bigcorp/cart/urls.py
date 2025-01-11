from django.urls import path 
from . import views


app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart-view'),
    path('add/', views.cart_add, name='add-to-cart'),
    path('delete/<slug:slug>/', views.cart_delete, name='cart-delete'),
    path('update/<slug:slug>/', views.cart_update, name='cart-update'),
    
]

from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutPage,name='logout'),
    path('user/',views.userPage,name='user'),
    path('register/',views.register,name='register'),
    path('products/',views.products,name='products'),
    path('all_orders/',views.allOrders,name='all_orders'),
    path('customer/<str:uid>/',views.customer,name='customer'),
    path('create_order/<str:uid>/',views.createOrder,name='create_order'),
    path('update_order/<str:uid>/',views.updateOrder,name='update_order'),
    path('delete_order/<str:uid>/',views.deleteOrder,name='delete_order'),
    path('create_customer/',views.createCustomer,name='create_customer'),
    path('update_customer/<str:uid>/',views.updateCustomer,name='update_customer'),
    path('delete_customer/<str:uid>/',views.deleteCustomer,name='delete_customer')
]

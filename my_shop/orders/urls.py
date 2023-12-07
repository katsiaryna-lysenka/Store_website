from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('my_orders/', views.my_orders, name='order_my_orders'),
]



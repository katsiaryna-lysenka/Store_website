from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('my_orders/', views.my_orders, name='order_my_orders'),
    # path('create/orders/my_orders/', views.my_orders, name='order_create_orders_my_orders'),
]


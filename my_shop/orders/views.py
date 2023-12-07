from django.core.checks import messages
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from django import forms
from typing import Tuple, Any
from cart.cart import Cart
from .forms import OrderCreateForm

from .models import OrderItem, UserOrders, User


def order_create(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            user_orders = UserOrders.objects.get(user=request.user)
            user_orders.orders.add(order)

            cart.clear()
            form = OrderCreateForm()
            if request.POST.get('pickup_or_delivery') == 'delivery':
                return render(request, 'created_delivery.html',
                              {'order': order, 'username': request.user.username, 'order_time': order.created,
                               'delivery_method': 'Доставка', 'delivery_address': order.address,
                               'message': 'Спасибо за заказ'})
            else:
                return render(request, 'created_pickup.html', {'order': order, 'username': request.user.username, 'order_time': order.created, 'delivery_method': 'Самовывоз', 'message': 'Ваш заказ в пути'})
    else:
        form = OrderCreateForm()
    form.fields['pickup_or_delivery'] = forms.ChoiceField(choices=[('pickup', 'Самовывоз'), ('delivery', 'Доставка')],
                                                          widget=forms.RadioSelect)
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})


@receiver(post_save, sender=User)
def create_user_orders(sender: Any, instance: User, created: bool, **kwargs: Any) -> None:
    if created:
        UserOrders.objects.create(user=instance)


@login_required
def my_orders(request: HttpRequest) -> HttpResponse:
    user_orders, created = UserOrders.objects.get_or_create(user=request.user)
    orders = user_orders.orders.all()
    return render(request, 'my_orders.html', {'orders': orders})













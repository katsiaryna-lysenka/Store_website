from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from . import forms
from .models import OrderItem, UserOrders
from .forms import OrderCreateForm
from cart.cart import Cart
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


def order_create(request):
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
            # Добавляю заказ в UserOrders пользователя
            user_orders = UserOrders.objects.get(user=request.user)
            user_orders.orders.add(order)

            # очистка корзины
            cart.clear()
            form = OrderCreateForm()
            if request.POST.get('pickup_or_delivery') == 'delivery':
                return render(request, 'created_delivery.html', {'message': 'Спасибо за заказ'})
            else:
                return render(request, 'created_pickup.html', {'message': 'Ваш заказ в пути'})
    else:
        form = OrderCreateForm()
    form.fields['pickup_or_delivery'] = forms.ChoiceField(choices=[('pickup', 'Самовывоз'), ('delivery', 'Доставка')],
                                                          widget=forms.RadioSelect)
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})


@receiver(post_save, sender=User)
def create_user_orders(sender, instance, created, **kwargs):
    if created:
        UserOrders.objects.create(user=instance)


@login_required
def my_orders(request):
    # Проверяю, существует ли объект UserOrders для пользователя
    user_orders, created = UserOrders.objects.get_or_create(user=request.user)

    # Получаю заказы пользователя
    orders = user_orders.orders.all()

    # Отправляю заказы в шаблон
    return render(request, 'my_orders.html', {'orders': orders})

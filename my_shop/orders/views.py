from django.shortcuts import render

from . import forms
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django import forms


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
            # очистка корзины
            cart.clear()
            form = OrderCreateForm()
            if request.POST.get('pickup_or_delivery') == 'delivery':
                return render(request, 'created_delivery.html', {'message': 'Спасибо за заказ'})
            else:
                return render(request, 'created_pickup.html', {'message': 'Ваш заказ в пути'})
    else:
        form = OrderCreateForm()
    form.fields['pickup_or_delivery'] = forms.ChoiceField(choices=[('pickup', 'Самовывоз'), ('delivery', 'Доставка')], widget=forms.RadioSelect)
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})


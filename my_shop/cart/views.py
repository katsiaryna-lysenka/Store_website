from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from typing import Union
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request: HttpRequest, product_id: int) -> Union[HttpResponse, HttpResponseRedirect]:
    REGISTRATION_LINK = "http://127.0.0.1:8000/login/"
    registration_message = f"Пожалуйста, пройдите <a href='{REGISTRATION_LINK}'>регистрацию</a>."
    if not request.user.is_authenticated:
        return HttpResponse(registration_message, status=401)  # Указала статус-код 401

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data  # Использовала более понятное имя для переменной
        cart.add(product=product,
                 quantity=form_data['quantity'],
                 update_quantity=form_data['update'])
    return redirect('cart:cart_detail')


def cart_remove(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


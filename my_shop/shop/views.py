from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from newsapi.newsapi_client import NewsApiClient

from .models import Category, Product, Comment
from cart.forms import CartAddProductForm, CommentForm

#для регистрации
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserRegisterForm, UserLoginForm
from typing import Optional


#для авторизации и деавторизации

from django.contrib.auth.views import LoginView, LogoutView


def product_list(request: HttpRequest, category_slug: Optional[str] = None) -> HttpResponse:
    category: Optional[Category] = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).select_related('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


#Переделала для создания комментариев

def product_detail(request: HttpRequest, id: int, slug: str) -> HttpResponse:
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    # List of active comments for this post
    cart_product_form = CartAddProductForm()
    comments = product.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current product to the comment
            new_comment.product = product
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'shop/product/detail.html',
                {'product': product,
                  'cart_product_form': cart_product_form,
                  'comments': comments,
                  'comment_form': comment_form})


#Переделала для создания новостного блога


def news(request: HttpRequest) -> HttpResponse:
    newsapi = NewsApiClient(api_key='4399405a879a4684a406a6815b50d7ea')
    top = newsapi.get_top_headlines(language='en')

    articles = top['articles']
    mylist = [(article['title'], article['description'], article['urlToImage'], article['publishedAt']) for article in articles]

    if not mylist:
        return render(request, 'news.html', context={"error": "No news found."})
    else:
        return render(request, 'news.html', context={"mylist": mylist})



#для регистрации

class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """
    form_class = UserRegisterForm
    success_url = '/'
    template_name = 'user_register.html'
    success_message = 'Вы успешно зарегистрировались. Можете войти на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context


#для авторизации

class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Авторизация на сайте
    """
    form_class = UserLoginForm
    template_name = 'user_login.html'
    next_page = '/'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context


#деавторизация

class UserLogoutView(LogoutView):
    """
    Выход с сайта
    """
    next_page = '/'






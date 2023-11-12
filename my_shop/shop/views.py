from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Comment
from cart.forms import CartAddProductForm, CommentForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


#Переделала для создания комментариев

def product_detail(request, id, slug):
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




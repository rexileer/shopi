from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView
from django.contrib import messages

from .models import Category, ProductProxy


# def products_view(request):
#     """
#     Return a list of all products.

#     This view shows all products, in a grid.
#     """
#     products = ProductProxy.objects.all()
#     return render(request, 'shop/products.html', {'products': products})

class ProductListView(ListView):
    model = ProductProxy
    context_object_name = 'products'
    paginate_by = 15
    
    def get_template_names(self):
        if self.request.htmx:
            return 'shop/components/product_list.html'
        return 'shop/products.html'

def product_detail_view(request, slug):
    product = get_object_or_404(ProductProxy.objects.select_related('category'), slug=slug)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            if product.reviews.filter(created_by=request.user).exists():
                messages.error(request, 'You have already reviewed this product')
            else:
                rating = request.POST.get('rating', 3)
                content = request.POST.get('content', '')
                if content:
                    product.reviews.create(rating=rating, content=content, created_by=request.user, product=product)
                    return redirect(request.path)
        else:
            messages.error(request, 'You must be logged in to review a product')

    context = {
        'product': product
    }
    
    return render(request, 'shop/product_detail.html', context)
                


def category_list(request, slug):
    """
    Return a list of products for a given category.

    This view shows all products associated with the given category, in a
    grid.
    """
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related('category').filter(category=category)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'shop/category_list.html', context)

def search_products(request):
    query = request.GET.get('q')
    products = ProductProxy.objects.filter(name__icontains=query).distinct()
    context = {
        'products': products,
    }
    if not query or not products:
        return redirect('shop:products')
    return render(request, 'shop/products.html', context)
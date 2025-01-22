from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

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
    """
    Return a detailed view of a product.

    This view shows the product in a form that is more detailed than the
    product list view.
    """
    product = get_object_or_404(ProductProxy, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})

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
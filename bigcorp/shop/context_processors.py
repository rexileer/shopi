from .models import Category

def categories(request):
    """
    Adds a list of categories to the context.

    Categories are the categories that are top-most in the tree, i.e. those
    that do not have a parent category.

    This context processor is used to add the categories to the base.html
    template, so that the categories can be listed in the navigation menu.
    """
    return {
        'categories': Category.objects.filter(parent=None)
    }
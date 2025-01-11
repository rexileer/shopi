from decimal import Decimal

from shop.models import ProductProxy


class Cart():
    def __init__(self, request):
        
        self.session = request.session
        
        cart = self.session.get('session_key')
        
        if not cart:
            cart = self.session['session_key'] = {}
            
        self.cart = cart
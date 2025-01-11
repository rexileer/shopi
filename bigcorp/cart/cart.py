from decimal import Decimal

from shop.models import ProductProxy


class Cart():
    def __init__(self, request):
        
        self.session = request.session
        
        cart = self.session.get('session_key')
        
        if not cart:
            cart = self.session['session_key'] = {}
            
        self.cart = cart
        
    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())
        
    def add(self, product, quantity):
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {'qty': quantity, 'price': str(product.price)}
            
        self.cart[product_id]['qty'] = quantity
        
        self.session.modified = True
        
    def save(self):
        self.session.modified = True
import json

from django.contrib.sessions.middleware import SessionMiddleware

from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from shop.models import Category, ProductProxy

from .views import cart_view, cart_add, cart_delete, cart_update


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory().get(reverse('cart:cart-view'))
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_view(self):
        request = self.factory
        response = cart_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.client.get(reverse('cart:cart-view')), 'cart/cart-view.html')
        
class CartAddViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='django')
        self.product = ProductProxy.objects.create(
            category=self.category,
            name='Product 1',
            price=10,
        )
        self.factory = RequestFactory().post(reverse('cart:add-to-cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 2
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_add_view(self):
        request = self.factory
        response = cart_add(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['qty'], 2)
        self.assertEqual(data['product'], 'Product 1')
        
        
class CartDeleteViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='django')
        self.product = ProductProxy.objects.create(
            category=self.category,
            name='Product 1',
            slug='product-1',
        )
        self.factory = RequestFactory().post(reverse('cart:delete-from-cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 2
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_delete_view(self):
        request = self.factory
        response = cart_delete(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['qty'], 0)


class CartUpdateViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Example Category')
        self.product = ProductProxy.objects.create(
            category=self.category,
            name='Example 1',
            price=10,
        )
        self.factory = RequestFactory().post(reverse('cart:add-to-cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 2
        })
        self.factory = RequestFactory().post(reverse('cart:update-cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 5
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_update_view(self):
        request = self.factory
        response = cart_add(request)
        response = cart_update(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['qty'], 5)
        self.assertEqual(data['total'], '50.00')

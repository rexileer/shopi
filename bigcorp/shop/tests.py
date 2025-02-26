from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Category, Product, ProductProxy


class ProductViewTest(TestCase):
    def test_get_products(self):
        
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='test_image.gif',
            content=small_gif,
            content_type='image/gif'
        )
        category = Category.objects.create(name='django')
        product_1 = Product.objects.create(
            category=category,
            name='Product 1',
            slug='product-1',
            image=uploaded,
        )
        product_2 = Product.objects.create(
            category=category,
            name='Product 2',
            slug='product-2',
            image=uploaded,
        )
        response = self.client.get(reverse('shop:products'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 2)
        products_in_context = sorted(response.context['products'], key=lambda p: p.id)
        self.assertEqual(products_in_context[0].id, product_1.id)
        self.assertEqual(products_in_context[1].id, product_2.id)
        self.assertContains(response, product_1)
        self.assertContains(response, product_2)
        
class ProductDetailViewTest(TestCase):
    def test_get_product_by_slug(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='test_image.gif',
            content=small_gif,
            content_type='image/gif'
        )
        category = Category.objects.create(name='django')
        product = Product.objects.create(
            category=category,
            name='Product 1',
            slug='product-1',
            image=uploaded,
        )
        response = self.client.get(reverse('shop:product-detail', args=[product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], product)
        self.assertEqual(response.context['product'].name, 'Product 1')
        self.assertEqual(response.context['product'].slug, 'product-1')
        self.assertContains(response, product)
        
class CategoryListViewTest(TestCase):
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='test_image.gif',
            content=small_gif,
            content_type='image/gif'
        )
        self.category = Category.objects.create(
            name='Test Category', 
            slug='test-category',
        )
        self.product = ProductProxy.objects.create(
            category=self.category,
            name='Test Product',
            slug='test-product',
            image=uploaded,
        )

    def test_status_code(self):
        response = self.client.get(reverse('shop:category-list', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        
    def test_template_used(self):
        response = self.client.get(reverse('shop:category-list', args=[self.category.slug]))
        self.assertTemplateUsed(response, 'shop/category_list.html')
        
    def test_context_data(self):
        response = self.client.get(reverse('shop:category-list', args=[self.category.slug]))
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['products'][0], self.product)
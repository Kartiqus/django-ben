from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product, Order

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'price': '9.99',
            'stock': 10
        }
        self.product = Product.objects.create(**self.product_data)

    def test_create_product(self):
        response = self.client.post('/api/products/', self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_product_list(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product = Product.objects.create(name='Test Product', price='9.99', stock=10)
        self.order_data = {
            'name': 'Test Customer',
            'email': 'test@example.com',
            'address': 'Test Address',
            'total_amount': '9.99',
            'items': [{'product': self.product.id, 'quantity': 1}]
        }

    def test_create_order(self):
        response = self.client.post('/api/orders/', self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_customer_orders(self):
        self.client.post('/api/orders/', self.order_data, format='json')
        response = self.client.get(f'/api/orders/customer_orders/?email={self.order_data["email"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
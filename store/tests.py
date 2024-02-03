# store/tests.py
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from .models import Item, Order, Discount, Tax

class StoreTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.item1 = Item.objects.create(name='Item 1', description='Description 1', price=10.00)
        self.item2 = Item.objects.create(name='Item 2', description='Description 2', price=20.00)
        self.order = Order.objects.create(name='Test Order')

    def test_item_detail_view(self):
        response = self.client.get(reverse('item_detail', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Description 1')

    def test_add_item_to_order_view(self):
        response = self.client.post(reverse('add_item_to_order', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.order.items.filter(pk=self.item1.id).exists())

    def test_remove_item_from_order_view(self):
        self.order.items.add(self.item1)
        response = self.client.post(reverse('remove_item_from_order', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.order.items.filter(pk=self.item1.id).exists())

    def test_order_detail_view(self):
        self.order.items.add(self.item1, self.item2)
        response = self.client.get(reverse('order_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Item 1')
        self.assertContains(response, 'Item 2')
        self.assertContains(response, f'Итого: ${self.order.get_total_cost()}')

    def test_buy_order_view(self):
        self.order.items.add(self.item1, self.item2)
        Discount.objects.create(order=self.order, amount=5.00)
        Tax.objects.create(order=self.order, amount=3.00)

        response = self.client.post(reverse('buy_order'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.order.get_total_cost(), Decimal('30.00'))
        self.assertEqual(self.order.discount.amount, Decimal('5.00'))
        self.assertEqual(self.order.tax.amount, Decimal('3.00'))

    def test_get_checkout_session_view(self):
        response = self.client.get(reverse('get_checkout_session', args=[self.item1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('session_id', response.json())
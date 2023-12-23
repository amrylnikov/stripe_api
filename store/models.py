from django.db import models
from django.urls import reverse


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_absolute_url(self):
        return reverse('item_detail', args=[str(self.id)])

class Order(models.Model):
    items = models.ManyToManyField(Item)
    name = models.CharField(max_length=255)

    def get_total_cost(self):
        return sum(item.price for item in self.items.all())

    def get_absolute_url(self):
        return reverse('order_detail')


class Discount(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Tax(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

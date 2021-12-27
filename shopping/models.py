from django.db import models


class Item(models.Model):
    """An item that can be purchased"""

    title = models.CharField(max_length=256)
    price = models.FloatField()

    def __str__(self) -> str:
        return f"{self.title} (${self.price})"


class Order(models.Model):
    """An order is a collection of items purchased"""


class ItemsOrder(models.Model):
    """Keeps track of the quantity of items purchased in an order"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    quantity = models.IntegerField()

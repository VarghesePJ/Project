from django.db import models
from Account.models import User
from Cart.models import CartItem

class Order(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "pending"),
        ("SUCCESS", "success"),
        ("FAILED", "failed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="PENDING")

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=250, null=True, blank=True)
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=100)
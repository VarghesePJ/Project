from django.db import models
from Account.models import User
from Store.models import Product
from django.utils.timezone import now

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name= 'cart')

    def __str__(self):
        return self.user.username
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity
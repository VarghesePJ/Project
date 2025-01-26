from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=250,unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='Images/Category')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=250,unique=True)
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='Images/Product')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_data = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
from django.db import models
from account.models import Customer, Address

# Create your models here.
class Category(models.Model):
    name = models.CharField()
    description = models.TextField()
    image = models.ImageField()
    is_active = models.BooleanField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,  null=True, blank=True)


class Product(models.Model):
    name = models.TextField(max_length=150, unique=True)
    image = models.ImageField(upload_to='product_pictures')
    description = models.TextField()
    best_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    rating = models.DecimalField()
    categories = models.ManyToManyField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField()
    def __str__(self):
        return self.name
    



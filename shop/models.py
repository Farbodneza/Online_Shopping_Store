from django.db import models
from account.models import CustomUser, Address

# Create your models here.
class Category(models.Model):
    name = models.CharField()
    description = models.TextField()
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,  null=True, blank=True)


class Product(models.Model):
    name = models.TextField(max_length=150, unique=True)
    description = models.TextField()
    best_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, default=0.0)
    categories = models.ManyToManyField(Category, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="محصول")
    image = models.ImageField(upload_to='product_images/', verbose_name="تصویر")
    

class Store(models.Model):
    name = models.CharField()
    description = models.TextField()
    seller = models.ForeignKey(Customer, related_name='store')


class Seller(models.Model):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE)


class StoreItem(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    

class Order(models.Model):
    STATUS_CHOCES = [
        (1, 'Pending'),
        (2, 'Processing'),
        (3, 'Delivered'),
        (4, 'Cancelled'),
        (5, 'FAILED'),
        
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOCES, default=1)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    store_item = models.ForeignKey(StoreItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price  = models.DecimalField(max_digits=10, decimal_places=2)



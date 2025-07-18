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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/', verbose_name="تصویر")
    

class Store(models.Model):
    name = models.CharField()
    description = models.TextField()
    seller = models.ForeignKey(CustomUser, related_name='store', on_delete=models.CASCADE)


class StoreItem(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    

class Order(models.Model):
    STATUS_CHOCES = [
        (1, 'Pending'),
        (2, 'Processing'),
        (3, 'Delivered'),
        (4, 'Cancelled'),
        (5, 'FAILED'),
        
    ]
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', default=None)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOCES, default=1)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    store_item = models.ForeignKey(StoreItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price  = models.DecimalField(max_digits=10, decimal_places=2)


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_discount(self):
        return sum(item.total_discount for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    store_item = models.ForeignKey('StoreItem', on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.store_item.product.name} in {self.cart.user.username}'s cart"

    @property
    def unit_price(self):
        return self.store_item.price

    @property
    def total_discount(self):
        if self.store_item.discount_price:
            return (self.store_item.price - self.store_item.discount_price) * self.quantity
        return 0

    @property
    def total_item_price(self):
        price = self.store_item.discount_price or self.store_item.price
        return price * self.quantity

    @property
    def total_price(self):
        return self.total_item_price


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField() 
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
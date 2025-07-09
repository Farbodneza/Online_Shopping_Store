from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Customer(AbstractUser):
    bio = models.TextField(blank=True,null=True)
    profile_picture = models.ImageField(upload_to=,blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    def set_primary_address(self, address_id):
        addresses = self.addresses.object.all()
        try:
            new_primary = addresses.get(id=address_id)
        except Address.DoesNotExist:
            raise ValueError("Address does not belong to this user")
        addresses.update(is_primary=False)
        new_primary.is_primary = True
        new_primary.save()


class Address(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=100)
    postal_code = models.PositiveIntegerField()
    city = models.CharField()
    country = models.CharField()
    address = models.TextField()
    is_primary = models.BooleanField()
    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"

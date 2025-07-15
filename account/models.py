from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True,null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures',blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    is_seller = models.BooleanField(default=False)
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=100)
    postal_code = models.PositiveIntegerField()
    country = models.CharField()
    city = models.CharField()
    state = models.CharField()
    address_line_1 = models.TextField()
    address_line_2 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField();
    is_primary = models.BooleanField()
    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"

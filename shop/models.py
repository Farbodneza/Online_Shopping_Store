from django.db import models
from account.models import Customer, Address

# Create your models here.
class Category(models.Model):
    name = models.CharField()
    description = models.TextField()
    image = models.ImageField()
    is_active = models.BooleanField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,  null=True, blank=True)




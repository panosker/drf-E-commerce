from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Category(MPTTModel):
    names = models.CharField(max_length=100, unique=True)
    # CONNECT in tree struture the catefories together
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["names"]

    def __str__(self):
        return self.names


class Brand(models.Model):
    names = models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self):
        return self.names


class Product(models.Model):
    names = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.names

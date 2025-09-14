from enum import Enum
from django.db import models

class ProductStatusEnum(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"

class Product(models.Model):
    sku = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_qty = models.IntegerField()
    status = models.CharField(max_length=20, choices=ProductStatusEnum.choices, default=ProductStatusEnum.INACTIVE)

    class Meta:
        ordering = ['sku']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.name} ({self.sku})"
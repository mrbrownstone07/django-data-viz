from uuid import uuid4
from django.db import models
from django.contrib import admin
from unfold.admin import ModelAdmin

from .products import Product
from .warehouses import Warehouse

class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    units = models.DecimalField(blank=False, default=0.00, null=False, decimal_places=2, max_digits=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.product.name
   
class StockAdmin(ModelAdmin):
    list_display = ["product", "warehouse", "units", "created", "updated"]
    search_fields = ("product", "warehouse")
    ordering = ("created", )  
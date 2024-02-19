from uuid import uuid4
from django.db import models
from django.contrib import admin
from django.http import HttpRequest
from unfold.admin import ModelAdmin
from inventory.models.products import Product

class MarketPriceData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    price = models.DecimalField(blank=False, null=False, decimal_places=2, max_digits=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product.name + "price at " + self.created.strftime('%m-%d-%Y %H:%M:%S')


class MarketPriceDataAdmin(ModelAdmin):
    list_display = ["id", "price", "product", "created", "updated"]
    search_fields = ("name", )
    ordering = ("created", ) 


    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        if request.user.is_superuser:
            return True
        return False
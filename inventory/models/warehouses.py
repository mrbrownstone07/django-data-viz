from uuid import uuid4
from django.db import models
from django.contrib import admin
from unfold.admin import ModelAdmin

class Warehouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=150, blank=False, null=False)
    address = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    
class WarehouseAdmin(ModelAdmin):
    list_display = ["name", "created", "updated"]
    search_fields = ("name", )
    ordering = ("created", )  
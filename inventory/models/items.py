from uuid import uuid4
from django.db import models
from django.contrib import admin
from .categories import Category
from unfold.admin import ModelAdmin

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=150, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
class ItemAdmin(ModelAdmin):
    list_display = ["id", "name", "category", "created", "updated"]
    search_fields = ("name", )
    ordering = ("created", )

    


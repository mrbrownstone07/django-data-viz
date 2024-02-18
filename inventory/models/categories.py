from uuid import uuid4
from django.db import models
from django.contrib import admin
from unfold.admin import ModelAdmin

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=150, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class InLineItems(admin.TabularInline):
    from .items import Item
    model = Item   
  
    
class CategoryAdmin(ModelAdmin):
    list_display = ["id", "name", "created", "updated"]
    search_fields = ("name", )
    ordering = ("created", ) 
    
    inlines = [InLineItems] 
    


    

    
from django.contrib import admin
from .models.categories import Category, CategoryAdmin
from .models.items import Item, ItemAdmin


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
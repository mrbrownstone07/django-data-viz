from django.contrib import admin
from .models.categories import Category, CategoryAdmin
from .models.products import Product, ProductAdmin
from .models.warehouses import Warehouse, WarehouseAdmin
from .models.product_inouts import ProductInOut, ProductInOutAdmin

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(ProductInOut, ProductInOutAdmin)
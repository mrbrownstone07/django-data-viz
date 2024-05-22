
from uuid import uuid4
from django.db import models
from datetime import datetime
from django.forms import Form
from django.http import HttpRequest
from inventory.models.products import Product
from inventory.models.warehouses import Warehouse
from unfold.admin import ModelAdmin
from unfold.decorators import display
from django.contrib.admin import DateFieldListFilter


class InOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order_id = models.IntegerField(unique=True, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    units = models.DecimalField(blank=False, default=0.00, null=False, decimal_places=2, max_digits=10)
    unit_price = models.DecimalField(blank=False, null=False, default=0.00, decimal_places=2, max_digits=10, verbose_name='Unit Price')
    total_price = models.DecimalField(blank=True, null=True, default=0.00, decimal_places=2, max_digits=10, verbose_name='total Price')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id)
                             
class InOrderAdmin(ModelAdmin):
    search_fields = ("product", )
    list_filter=['warehouse', 'product', ('created', DateFieldListFilter),]
    
    ordering = ("-created", )
    readonly_fields=("total_price", "order_id")
    list_display = [
        "order_id",
        "product", 
        "warehouse", 
        "show_units_ordered", 
        "unit_price", 
        "total_price", 
    ]
    
    @display(
        description="units Ordered", label=True
    )
    def show_units_ordered(self, obj):
        return obj.units, obj.product.unit
    
    def save_model(self, request: HttpRequest, obj: models.Model, form: Form, change) -> None:            
        obj.total_price = (obj.unit_price * obj.units)
        obj.order_id = int(f"11{datetime.now().strftime('%d%m%y%H%M%S')}")      
        return super().save_model(request, obj, form, change)
    
    def has_view_permission(self, request: HttpRequest, obj=None) -> bool:
        return super().has_view_permission(request, obj)
    
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        if request.user.is_superuser:
            return True
        
        if obj:
            if obj.delivered:
                return False
            
        return True 
    


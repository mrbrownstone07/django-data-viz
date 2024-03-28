
from uuid import uuid4
from django import forms
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.forms import Form, ValidationError
from django.http import HttpRequest
from .products import Product
from django.contrib import admin
from .categories import Category
from .warehouses import Warehouse
from unfold.admin import ModelAdmin
from unfold.decorators import display
from django.contrib.admin import DateFieldListFilter

IN_ORDER = 1
OUT_ORDER = 2

IN_OUT_FLAG = ( 
    (IN_ORDER, "Inbound Order"), 
    (OUT_ORDER, "Outbound Order"), 
) 

class ProductInOut(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    order_type = models.IntegerField(choices=IN_OUT_FLAG, default=IN_ORDER, verbose_name='Order Type')
    units = models.DecimalField(blank=False, default=0.00, null=False, decimal_places=2, max_digits=10)
    unit_price = models.DecimalField(blank=False, null=False, default=0.00, decimal_places=2, max_digits=10, verbose_name='Unit Price')
    total_price = models.DecimalField(blank=True, null=True, default=0.00, decimal_places=2, max_digits=10, verbose_name='total Price')
    discount = models.DecimalField(blank=True, null=True, default=0.00, decimal_places=2, max_digits=10, verbose_name='Discount in Taka')
    order_initiated_on = models.DateTimeField(auto_now_add=True, verbose_name='Order Initiated On')
    order_completed_on = models.DateTimeField(blank=True, null=True, verbose_name='Order Completed On')
    delivered = models.BooleanField(default=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id) 
    
    def clean(self):
        if self.order_type == OUT_ORDER:
            from .stock import Stock
            available_stock = Stock.objects.filter(product=self.product, warehouse=self.warehouse)
            if not available_stock:
                raise ValidationError(f'{self.product} is not available at {self.warehouse}.')
        
            if self._state.adding:    
                check = available_stock[0].units - self.units
            else:
                current_units = ProductInOut.objects.get(id=self.id).units
                check = available_stock[0].units - self.units + current_units

            if check < 0:
                raise ValidationError(f'{self.units} of {self.product} is not available at {self.warehouse}.')            

                             
class ProductInOutAdmin(ModelAdmin):
    search_fields = ("product", )
    list_filter=['warehouse', 'order_type', 'product', ('created', DateFieldListFilter),]
   
    ordering = ("-created", )
    readonly_fields=("order_initiated_on", "order_completed_on", "total_price",)
    list_display = [
        "product", 
        "warehouse", 
        "show_order_type", 
        "show_units_ordered", 
        "unit_price", 
        "total_price", 
        "show_delivery_status", 
        "order_initiated_on", 
        "order_completed_on", 
    ]
    
    @display(
        description="units Ordered", label=True
    )
    def show_units_ordered(self, obj):
        return obj.units, obj.product.unit
    
    @display(
        description="Delivery Status", label={"Delivered": "success",  "Not Delivered": "danger"}
    )
    def show_delivery_status(self, obj):
        if obj.delivered:
            return "Delivered"
        return "Not Delivered"
    
    @display(
        description="Order Type", label={"Inbound": "info",  "Outbound": "warning"}
    )
    def show_order_type(self, obj):
        if obj.order_type == 1:
            return "Inbound"
        return "Outbound"
    
        
    def save_model(self, request: HttpRequest, obj: models.Model, form: Form, change) -> None:
        if obj.delivered and not obj.order_completed_on:
            obj.order_completed_on = datetime.now(tz=timezone.get_current_timezone())  
            
        obj.total_price = (obj.unit_price * obj.units) - obj.discount
               
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
    


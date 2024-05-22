
from uuid import uuid4
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.forms import Form, ValidationError
from django.http import HttpRequest
from django.contrib import admin 
from inventory.models.products import Product
from inventory.models.warehouses import Warehouse
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.decorators import display
from django.contrib.admin import DateFieldListFilter
from django.db.models import Sum

PAID = 1
UNPAID = 2
PARTIAL = 3

PAYMENT_STATUS = ( 
    (PAID, "Paid"), 
    (UNPAID, "Unpaid"),  
    (PARTIAL, "Partial Payment"), 
) 

PAYMENT_STATUS_MAP = {
    1: "Paid",
    2: "Unpaid",
    3: "Partial Payment",
}


class OutOrder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order_id = models.IntegerField(unique=True, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    buyer = models.CharField(max_length=255, blank=False, null=False)
    delivery_address= models.TextField()
    location = models.CharField(max_length=255, blank=False, null=False)
    units = models.DecimalField(blank=False, default=0.00, null=False, decimal_places=2, max_digits=10)
    unit_price = models.DecimalField(blank=False, null=False, default=0.00, decimal_places=2, max_digits=10, verbose_name='Unit Price')
    total_price = models.DecimalField(blank=True, null=True, default=0.00, decimal_places=2, max_digits=10, verbose_name='total Price')
    discount = models.DecimalField(blank=True, null=True, default=0.00, decimal_places=2, max_digits=10, verbose_name='Discount in Taka')
    order_initiated_on = models.DateTimeField(auto_now_add=True, verbose_name='Order Initiated On')
    tentative_delivery_date = models.DateTimeField(blank=True, null=True, verbose_name='Requested Delivery Date')
    payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=UNPAID, verbose_name='Payment Status')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.id) 
    
    def clean(self):
        from inventory.models.stock import Stock
        available_stock = Stock.objects.filter(product=self.product, warehouse=self.warehouse)
        if not available_stock:
            raise ValidationError(f'{self.product} is not available at {self.warehouse}.')
    
        if self._state.adding:    
            check = available_stock[0].units - self.units
        else:
            current_units = OutOrder.objects.get(id=self.id).units
            check = available_stock[0].units - self.units + current_units

        if check < 0:
            raise ValidationError(f'{self.units} of {self.product} is not available at {self.warehouse}.')        
        
class PaymentsInline(TabularInline):
    from .payments import Payment
    model = Payment    

                             
class OutOrderAdmin(ModelAdmin):
    search_fields = ("product", )
    list_filter=['warehouse', 'product', ('created', DateFieldListFilter),]
    inlines = [PaymentsInline]
    ordering = ("-created", )
    readonly_fields=("order_initiated_on", "order_id", "total_price",)
    list_display = [
        "product",
        "buyer",
        "warehouse", 
        "show_units_ordered", 
        "unit_price", 
        "total_price",
        # "show_payment_details",
        "show_payment_status", 
        "order_initiated_on", 
        "tentative_delivery_date", 
    ]
    
    
    @display(
        description="Payments", label=True
    )
    def show_payment_details(self, obj):
        from .payments import Payment
        paid_amount = Payment.objects.filter(out_order=obj.id).annotate(total_paid=Sum('amount')).values()
        print(paid_amount)
        return f"paid: {paid_amount['total_paid']}", f"Due: {(obj.total_price) - paid_amount['total_paid']}"
    @display(
        description="units Ordered", label=True
    )
    def show_units_ordered(self, obj):
        return obj.units, obj.product.unit
    
    @display(
        description="Payment Status", label={"Paid": "success",  "Unpaid": "danger", "Partial Payment": "info"}
     )
    def show_payment_status(self, obj):
        return PAYMENT_STATUS_MAP[obj.payment_status]
   
    def save_model(self, request: HttpRequest, obj: models.Model, form: Form, change) -> None:   
        from .payments import Payment
        obj.total_price = (obj.unit_price * obj.units) - obj.discount
        obj.order_id = int(f"55{datetime.now().strftime('%d%m%y%H%M%S')}")          
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
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models.product_inouts import ProductInOut, IN_ORDER, OUT_ORDER
from .models.stock import Stock
from django.db.models import F

@receiver(pre_save, sender=ProductInOut,  dispatch_uid="update_stock")
def update_stock(sender, instance, **kwargs):
    
    product_inout_record = ProductInOut.objects.filter(id = instance.id)
    
    is_delivery_flag_already_true = True
    is_order_completion_date_set = True
    delivery_completion = False
    order_units_changed = False
    out_order_units_changed = False
    
    if product_inout_record:
        current_units = product_inout_record[0].units
        is_delivery_flag_already_true = product_inout_record[0].delivered
        is_order_completion_date_set = False if product_inout_record[0].order_completed_on == None else True 
        
        delivery_completion = not is_delivery_flag_already_true and not is_order_completion_date_set and instance.delivered 
        order_units_changed = current_units != instance.units and instance.delivered
        out_order_units_changed = current_units != instance.units
        
        
    # if instance._state.adding or instance.delivered:
    if (instance._state.adding and instance.order_type == OUT_ORDER):
        Stock.objects.update(
            product=instance.product,
            warehouse=instance.warehouse,
            units=F('units') - instance.units 
        )  
    
    elif (not instance._state.adding and instance.order_type == OUT_ORDER and out_order_units_changed):
        stock = Stock.objects.get(
            product=instance.product,
            warehouse=instance.warehouse            
        )
        stock.units = F('units') - instance.units + current_units        
        stock.save()
    
    elif (
        instance.order_type == IN_ORDER
        and (
           delivery_completion
           or order_units_changed 
           or (instance._state.adding and instance.delivered)
        )
    ):                     
        stock, created = Stock.objects.get_or_create(
            product=instance.product,
            warehouse=instance.warehouse,              
        )
        
        if order_units_changed:
            stock.units = F('units') + instance.units - current_units
        else:   
            stock.units = F('units') + instance.units
        
        stock.save()
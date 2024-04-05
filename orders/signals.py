from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models.out_orders import OutOrder
from .models.payments import Payment
from django.db.models import F

@receiver(post_save, sender=Payment,  dispatch_uid="update_stock")
def update_stock(sender, instance, **kwargs):
    
    product_inout_record = ProductInOut.objects.filter(id = instance.id)
    order_units_changed = False
    
    if product_inout_record:
        current_units = product_inout_record[0].units
        order_units_changed = current_units != instance.units 
    
    # Logic for reudcing the stock on OutOrder creation. 
    if (instance._state.adding 
        and (instance.order_type == OUT_ORDER or order_units_changed)):
        
        stock = Stock.objects.get(
            product=instance.product,
            warehouse=instance.warehouse,
        )
        stock.units = F('units') - instance.units + current_units if order_units_changed else F('units') - instance.units      
        stock.save()
    
    # Logic for Upading sotck on Inorder creation and inorder update.
    elif (instance.order_type == IN_ORDER 
        and (order_units_changed or instance._state.adding)): 
                            
        stock, created = Stock.objects.get_or_create(
            product=instance.product,
            warehouse=instance.warehouse,              
        )
        stock.units = F('units') + instance.units - current_units if order_units_changed else F('units') + instance.units
        stock.save()
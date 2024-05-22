from django.contrib import admin
from .models.in_orders import InOrder, InOrderAdmin
from .models.out_orders import OutOrder, OutOrderAdmin
from .models.payments import Payment

admin.site.register(InOrder, InOrderAdmin)
admin.site.register(OutOrder, OutOrderAdmin)
admin.register(Payment)

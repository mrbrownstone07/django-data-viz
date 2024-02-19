from django.contrib import admin
from .models.mrp_data import MarketPriceData, MarketPriceDataAdmin

# Register your models here.

admin.site.register(MarketPriceData, MarketPriceDataAdmin)

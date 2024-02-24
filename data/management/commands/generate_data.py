import random
from django.utils import timezone
from datetime import datetime, timedelta
from inventory.models.products import Product
from data.models.mrp_data import MarketPriceData
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generates random data set for market price of the products present in the Product Model"
    def handle(self, *args, **options):
        generate_market_price_data()
        

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) * 24):
        yield start_date + timedelta(hours=n)
    
def generate_market_price_data():
    products = Product.objects.all()
    
    
    start_date = datetime.now(tz=timezone.get_current_timezone()) + timedelta(days=-60)
    end_date = datetime.now(tz=timezone.get_current_timezone())
    
    for n in daterange(start_date, end_date):
        for product in products:
            MarketPriceData.objects.create(
                product=product,
                price=random.randint(112, 389)/10,
                created=n,
                updated=n
            )
            
    

        

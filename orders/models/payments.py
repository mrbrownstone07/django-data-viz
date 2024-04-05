from uuid import uuid4
from django.db import models
from .out_orders import OutOrder


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    amount = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
    out_order = models.ForeignKey(OutOrder, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.out_order.order_id) + " paid " + str(self.amount)+ " price at " + self.created.strftime('%m-%d-%Y %H:%M:%S')
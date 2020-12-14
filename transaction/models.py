from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class OrderCoins(models.Model):
    user = models.ForeignKey(User, related_name="OrderCoins" , on_delete=models.CASCADE)
    amount = models.IntegerField()
    order_id = models.CharField(max_length=100)
    reference_id = models.CharField(max_length=500 , blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class SellCoins(models.Model):
    user = models.ForeignKey(User, related_name="SellCoins" , on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    payment_mode = models.CharField(max_length=100 , default="Paytm")
    number = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    trasaction_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    
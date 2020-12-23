from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from accounts.models import *
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
    


class Penalty(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    reason = models.CharField(max_length=1000 , blank=True , null=True)
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=Penalty)
def penalty_handler(sender , instance,created,**kwargs): 
    profile = Profile.objects.filter(user = instance.user).first()
    profile.coins -= instance.amount
    profile.save()
    
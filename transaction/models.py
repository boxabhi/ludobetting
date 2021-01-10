from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from accounts.models import *
from django.utils.html import format_html
# Create your models here.




class OrderCoinRequest(models.Model):
    amount = models.IntegerField()
    order_id = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

@receiver(post_save, sender=OrderCoinRequest)
def order_handler(sender , instance,created,**kwargs):
    if instance.is_approved: 
        profile = Profile.objects.filter(user = instance.user).first()
        profile.coins += instance.amount
        profile.save()    
    

class PaytmOrderId(models.Model):
    amount = models.IntegerField()
    order_id = models.CharField(max_length=255 , unique=True)
    is_used = models.BooleanField(default=False)
    used_by = models.ForeignKey(User , on_delete=models.CASCADE , blank=True , null=True)
    created = models.DateTimeField(auto_now_add=True)



class OrderCoins(models.Model):
    user = models.ForeignKey(User, related_name="OrderCoins" , on_delete=models.CASCADE)
    amount = models.FloatField()
    order_id = models.CharField(max_length=100)
    reference_id = models.CharField(max_length=500 , blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class SellCoins(models.Model):
    user = models.ForeignKey(User, related_name="SellCoins" , on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    payment_mode = models.CharField(max_length=100 , default="Paytm")
    number = models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    trasaction_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    
    
    def pre_payment_mode(self):
        return format_html(
            '<span style="background-color:green,padding:3px">'+ self.payment_mode +'</span>',
           
        )
        #return self.payment_mode

    def user_register_number(self):
        number = Profile.objects.filter(user = self.user).first()
        return self.number


    def __str__(self):
        if self.is_paid :
            text = ' Paid'
        else:
            text = ' Not paid'
            
        return self.user.username + ' requested ' + str(self.amount) + text
    

class Penalty(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    reason = models.CharField(max_length=1000 , blank=True , null=True)
    created_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.user.username

class CashFree(models.Model):
    url = models.CharField(max_length=1000)
    app_id = models.CharField(max_length=100)
    secret = models.CharField(max_length=1000)
    use = models.BooleanField(default=False)


class ReffralBonous(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    reason = models.CharField(max_length=100 , blank=True ,null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " got " + str(self.amount)


@receiver(post_save, sender=Penalty)
def penalty_handler(sender , instance,created,**kwargs): 
    profile = Profile.objects.filter(user = instance.user).first()
    profile.coins -= instance.amount
    profile.save()
    
# @receiver(post_save, sender=Penalty)
# def sell_coin_handler(sender, instance, created , **kwargs):
#     if instance.is_paid:
#         profile = Profile.objects.filter(user = instance.user)
#         profile.coins += instance.amount
#         profile.save()
        
        
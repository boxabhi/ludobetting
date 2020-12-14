from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime
from django.db.models.signals import pre_save , post_save
from django.dispatch import receiver
from django.utils import timezone



class Profile(models.Model):
    user = models.ForeignKey(User , related_name="Profile", on_delete=models.CASCADE)
    whatsapp = models.CharField(max_length=15)
    coins = models.IntegerField(default=50)
    otp = models.CharField(max_length=10 , blank=True , null=True)
    is_verified = models.BooleanField(default=False)
    referral_by = models.ForeignKey(User, null=True, blank=True ,on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    



    
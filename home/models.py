from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Banners(models.Model):
    image = models.ImageField(upload_to = 'banners')

    


class Mobile(models.Model):
    text = models.CharField(max_length=100 , blank=True)
    mobile = models.CharField(max_length=100 , blank=True)
    
    def __str__(self):
        return self.mobile


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    amount = models.FloatField(default=0)
    history_type = models.CharField(max_length=100 , default="PLUS")
    created_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return str(self.amount)   
    

class TopWinners(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="winners")
    amount = models.IntegerField()
    
    def __str__(self):
        return self.name 



class Help(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    problem = models.TextField()
    
    def __str__(self):
        return self.name + ' asked for help'

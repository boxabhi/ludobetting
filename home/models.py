from django.db import models

# Create your models here.



class Banners(models.Model):
    image = models.ImageField(upload_to = 'banners')

    


class Mobile(models.Model):
    text = models.CharField(max_length=100 , blank=True)
    mobile = models.CharField(max_length=100 , blank=True)
    
    def __str__(self):
        return self.mobile
    
    

class TopWinners(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="winners")
    amount = models.IntegerField()
    
    def __str__(self):
        return self.name 



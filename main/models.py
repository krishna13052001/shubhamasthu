from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    branch = models.CharField(max_length=10,choices=(('Tirupati','Tirupati'),('Nellore','Nellore'),('Vijayawada','Vijayawada')))

class Cards(models.Model):
    
    code = models.CharField(max_length=10)
    amount = models.IntegerField()
    scratched = models.BooleanField(default=False)
    redeemed = models.BooleanField(default=False)
    redeemed_date = models.DateTimeField(blank=True,null=True)
    
class Coupon(models.Model):
    name = models.CharField(max_length=200)
    bill_id = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null = True)
    mobile = models.BigIntegerField()
    no_of_coupons = models.IntegerField()
    bill_amount = models.IntegerField()
    link = models.CharField(max_length=20)
    cards = models.ManyToManyField(Cards,related_name='coupon')
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class SiteAnnouncements(models.Model):
    message = models.CharField(max_length=500)
    link_exist = models.BooleanField()
    link = models.CharField(max_length=500,null=True,blank=True)
    date = models.DateField(auto_now_add=True,null=True)

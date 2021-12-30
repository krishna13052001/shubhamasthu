from django.db import models
from django.db.models.fields import related
from main.models import User
# from .main import User
# Create your models here.
class CouponCount(models.Model):
    nellore_count = models.IntegerField(default=0)
    tirupati_count = models.IntegerField(default=0)

class Cards(models.Model):
    code = models.CharField(max_length=10)
    scratched = models.BooleanField(default=False)
    redeemed = models.BooleanField(default=False)
    redeemed_date = models.DateTimeField(blank=True,null=True)
    luckycard_issued_by = models.ForeignKey(User,related_name = "luckycard_issued_by" ,on_delete=models.CASCADE, null = True, blank = True)
    
class Coupon(models.Model):
    name = models.CharField(max_length=200)
    bill_id = models.CharField(max_length=200,unique= True)
    email = models.EmailField(blank=True, null = True)
    mobile = models.BigIntegerField()
    no_of_coupons = models.IntegerField()
    # bill_amount = models.IntegerField()
    bill_amount = models.CharField(max_length = 200)
    link = models.CharField(max_length=20)
    lucky_cards = models.ManyToManyField(Cards,related_name='lucky_cards')
    lucky_created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name = "lucky_created_by")
    date_created = models.DateTimeField(auto_now_add=True)

class Winner(models.Model):
    winner_coupon = models.ForeignKey(Coupon,on_delete=models.CASCADE,related_name='winner_coupon_id')
    winner_card = models.ForeignKey(Cards,on_delete=models.CASCADE,related_name="winner_card_id")
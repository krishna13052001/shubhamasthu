from django.contrib import admin
from .models import User,Coupon,Cards
# Register your models here.
admin.site.register(User)
admin.site.register(Coupon)
admin.site.register(Cards)
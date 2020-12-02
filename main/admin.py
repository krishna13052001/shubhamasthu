from django.contrib import admin
from .models import User,Coupon,Cards,SiteAnnouncements
# Register your models here.
class CouponRef(admin.ModelAdmin):
    list_display = ['name','bill_id','mobile','bill_amount','no_of_coupons','created_by','date_created']
    list_filter = ['bill_id','mobile','no_of_coupons','date_created','created_by']
class CardRef(admin.ModelAdmin):
    list_display = ['amount','code','scratched','redeemed','redeemed_date']
    list_filter = ['amount','code','scratched','redeemed','redeemed_date']

class SARef(admin.ModelAdmin):
    list_display = ['date','message']

#link models to admin dashboard
admin.site.register(User)
admin.site.register(Coupon,CouponRef)
admin.site.register(Cards,CardRef)
admin.site.register(SiteAnnouncements,SARef)
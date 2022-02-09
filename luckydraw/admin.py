from django.contrib import admin
from .models import Cards,Coupon,CouponCount, DeletedNumber,Winner

# Register your models here.
class CouponRef(admin.ModelAdmin):
    list_display = ['name','bill_id','mobile','bill_amount','no_of_coupons','lucky_created_by','date_created']
    # list_filter = ['bill_id','mobile','no_of_coupons','date_created','lucky_created_by']
    list_filter = ['date_created','lucky_created_by']
class CardRef(admin.ModelAdmin):
    list_display = ['code','scratched','redeemed','redeemed_date']
    list_filter = ['code','scratched','redeemed','redeemed_date']
class CouponCountRef(admin.ModelAdmin):
    list_display = ['tirupati_count','nellore_count','vijayawada_count']
class WinnerRef(admin.ModelAdmin):
    list_display = ('winner_code','winner_coupon_name','winner_coupon_mobile','message')
    list_filter = ('winner_card__code',)
    def winner_code(self, instance):
        return instance.winner_card.code
    def winner_coupon_name(self, instance):
        return instance.winner_coupon.name
    def winner_coupon_mobile(self, instance):
        return instance.winner_coupon.mobile
class DeleteNumberRef(admin.ModelAdmin):
    list_display = ['code','branch']
#link models to admin dashboard
admin.site.register(Coupon,CouponRef)
admin.site.register(Cards,CardRef)
admin.site.register(CouponCount,CouponCountRef)
admin.site.register(Winner,WinnerRef)
admin.site.register(DeletedNumber,DeleteNumberRef)
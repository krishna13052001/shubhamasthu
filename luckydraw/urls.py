from django.urls import path,include
from . import views
urlpatterns = [
    path('dashboard',views.dashboard,name='dashboard'),
    path('validateOtp',views.validateOtp,name="validateOtp"),
    path('addCoupon',views.addCoupon,name="addCoupon"),
    path('validateMobileNumber',views.validateMobileNumber,name="validateMobileNumber"),
    path('scratch/<str:token>',views.scratch,name="scratch"),
    path('cardScratched/<int:id>',views.cardScratched,name="cardScratched"),
    path('redeemCoupon',views.redeemCoupon,name="redeemCoupon"),
    path('daily',views.daily,name="redeemCoupon"),
    path('weekly',views.weekly,name="redeemCoupon"),
    path('redeemotp',views.redeemotp,name="redeemotp"),
    path('validateCoupon',views.validateCoupon,name="validateCoupon"),
]

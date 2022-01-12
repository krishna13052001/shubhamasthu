from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('login',views.login,name="login"),
    # path('register',views.register,name="register"),
    path('changePassword',views.changePassword,name="changePassword"),
    path('validateOtp',views.validateOtp,name="validateOtp"),
    path('setNewPassword',views.setNewPassword,name="setNewPassword"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('logout',views.logout,name="logout"),
    path('addCoupon',views.addCoupon,name="addCoupon"),
    path('validateCoupon',views.validateCoupon,name="validateCoupon"),
    path('downStats',views.downStats,name="downStats"),
    path('redeemData',views.redeemData,name="redeemData"),
    path('scratch/<str:token>',views.scratch,name="scratch"),
    path('cardScratched/<int:id>',views.cardScratched,name="cardScratched"),
    path('redeem',views.redeem,name="redeem"),
    path('markRedeem',views.markRedeem,name="markRedeem"),
    path('redeemAmount', views.redeemAmount, name="reddemAmount"),
    path('empty',views.empty,name="empty"),
    path('vaildateotp',views.vaildateotp,name="vaildateotp")
]
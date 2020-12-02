from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('login',views.login,name="login"),
    path('register',views.register,name="register"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('logout',views.logout,name="logout"),
    path('addCoupon',views.addCoupon,name="addCoupon"),
    path('validateCoupon',views.validateCoupon,name="validateCoupon"),
    path('downStats',views.downStats,name="downStats"),
    path('scratch/<str:token>',views.scratch,name="scratch")
    #path('thanks',views.thanks,name="thanks")
]

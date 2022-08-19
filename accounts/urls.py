from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('loginpage/',views.loginpage,name='loginpage'),
    path('register',views.register,name='register'),
    path('logoutUser',views.logoutUser,name='logoutUser'),
    path('userdash',views.userdash,name='userdash'),
    path('editprofile',views.editprofile,name='editprofile'),
    path('order_detail/<int:order_id>/', views.order_detail, name="order_detail"),
    path('cancel_order/<int:order_id>',views.cancel_order,name='cancel_order'),
]
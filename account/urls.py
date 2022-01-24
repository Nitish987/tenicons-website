from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginacc, name='loginacc'),
    path('createacc/', views.createacc, name='createacc'),
    path('logoutacc/', views.logoutacc, name='logoutacc'),
    # API
    path('changeotpstate/', views.changeotpstate, name='changeotpstate'),
    path('sendotp/', views.sendotp, name='sendotp'),
]

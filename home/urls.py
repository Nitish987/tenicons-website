from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('profile/', views.profile, name='profile'),
    path('uploads/', views.uploads, name='uploads'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # API
    path('edituploads/', views.edituploads, name='edituploads'),
    path('showuploads/', views.showuploads, name='showuploads'),
    path('showitemdetails/', views.showitemdetails, name='showitemdetails'),
    path('createlike/', views.createlike, name='createlike'),
    path('download/', views.download, name='download'),
]

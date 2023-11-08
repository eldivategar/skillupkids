from django.urls import path
from app.landing_page import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),    
    path('class-list/', views.class_list, name='class_list'),    
]
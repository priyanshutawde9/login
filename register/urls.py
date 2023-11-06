from django.urls import path
from register import  views


urlpatterns = [
    path('register/', views.Registration, name='registration'),
    path('login/', views.login_user, name='login'),
    
]

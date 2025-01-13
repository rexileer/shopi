from django.shortcuts import render
from django.urls import path 
from . import views


app_name = 'account'

urlpatterns = [
    # Registration and Verification
    
    path('register/', views.register_view, name='register'),
    path('email-verification/', 
        lambda request:render(request, 'account/registration/email-verification.html'),
        name='email-verification',
        ),
    
]

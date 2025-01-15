from django.shortcuts import render
from django.urls import path 
from . import views


app_name = 'account'

urlpatterns = [
    # Registration and Verification
    
    path('register/', views.register_view, name='register'),
    path('email-verification/', 
        lambda request:render(request, 'account/email/email-verification.html'),
        name='email-verification',
        ),
    
    # Login and Logout
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile-management/', views.profile_management_view, name='profile-management'),
    path('account-delete/', views.account_delete, name='account-delete'),
    
]

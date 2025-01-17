from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import path, reverse_lazy

from . import views


app_name = 'account'

urlpatterns = [
    # Registration and Verification

    path('register/', views.register_view, name='register'),
    path('email-verification/',
         lambda request: render(
             request, 'account/email/email-verification.html'),
         name='email-verification',
         ),

    # Login and Logout

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard

    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile-management/', views.profile_management_view,
         name='profile-management'),
    path('account-delete/', views.account_delete, name='account-delete'),

    # Password reset

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password/password_reset.html',
        email_template_name='account/password/password_reset_email.html',
        success_url=reverse_lazy('account:password_reset_done'),
    ),
        name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password/password_reset_done.html'),
        name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password/password_reset_confirm.html',
        success_url=reverse_lazy('account:password_reset_complete'),
    ),
        name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password/password_reset_complete.html'
    ),
        name='password_reset_complete'),
]

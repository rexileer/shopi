from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django_email_verification import send_email

User = get_user_model()

from .forms import UserCreateForm


def register_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')
            
            user = User.objects.create_user(
                username=user_username, email=user_email, password=user_password
            )
            
            user.is_active = False
            
            send_email(user)
            
            return redirect(request, '/account/email-verification/')
    else:
        form = UserCreateForm()
    return render(request, 'account/registration/register.html', {'form': form})

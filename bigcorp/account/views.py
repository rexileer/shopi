from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django_email_verification import send_email

User = get_user_model()

from .forms import UserCreateForm, UserLoginForm, UserUpdateForm


# Registration
def register_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            user_username = form.cleaned_data.get('username')
            user_password = form.cleaned_data.get('password1')
            
            # Create user
            user = User.objects.create_user(
                username=user_username, email=user_email, password=user_password
            )
            
            user.is_active = False
            
            send_email(user)
            
            return redirect('/account/email-verification/')
    else:
        form = UserCreateForm()
    return render(request, 'account/registration/register.html', {'form': form})


# Login
def login_view(request):
    
    form = UserLoginForm(request.POST or None)
    
    if request.user.is_authenticated:
        return redirect('shop:products')
    
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('account:dashboard')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('account:login')
            
    context = {
        'form': form
    }
    return render(request, 'account/login/login.html', context)


# Logout
def logout_view(request):
    logout(request)
    return redirect('shop:products')

@login_required(login_url='account:login')
def dashboard_view(request):
    return render(request, 'account/dashboard/dashboard.html')

@login_required(login_url='account:login')
def profile_management_view(request):
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('account:dashboard')
    else:
        form = UserUpdateForm(instance=request.user)
        
    context = {
        'form': form
    }
    
    return render(request, 'account/dashboard/profile-management.html', context)


@login_required(login_url='account:login')
def account_delete(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.delete()
        return redirect('shop:products')
    return render(request, 'account/dashboard/account-delete.html')
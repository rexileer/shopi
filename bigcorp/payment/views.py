from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse

from cart.cart import Cart

from .forms import ShippingAdressForm
from .models import ShippingAdress, Order, OrderItem


@login_required(login_url='account:login')
def shipping_view(request):
    try:
        shipping_adress = ShippingAdress.objects.get(user=request.user)
    except ShippingAdress.DoesNotExist:
        shipping_adress = None
        
    form = ShippingAdressForm(instance=shipping_adress)
    
    if request.method == 'POST':
        form = ShippingAdressForm(request.POST, instance=shipping_adress)
        if form.is_valid():
            shipping_adress = form.save(commit=False)
            shipping_adress.user = request.user
            shipping_adress.save()
            return redirect('account:dashboard')
    
    context = {
        'form': form,
    }
    return render(request, 'payment/shipping.html', context)


def checkout_view(request):
    return render(request, 'payment/checkout.html')


def complete_order_view(request):
    return render(request, 'payment/complete-order.html')


def payment_success_view(request):
    return render(request, 'payment/payment-success.html')


def payment_fail_view(request):
    return render(request, 'payment/payment-fail.html')
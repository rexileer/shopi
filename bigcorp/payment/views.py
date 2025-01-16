from django.shortcuts import render


def shipping_view(request):
    return render(request, 'payment/shipping.html')


def checkout_view(request):
    return render(request, 'payment/checkout.html')


def complete_order_view(request):
    return render(request, 'payment/complete-order.html')


def payment_success_view(request):
    return render(request, 'payment/payment-success.html')


def payment_fail_view(request):
    return render(request, 'payment/payment-fail.html')
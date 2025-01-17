from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse

from cart.cart import Cart

from .forms import ShippingAddressForm
from .models import ShippingAddress, Order, OrderItem


@login_required(login_url='account:login')
def shipping_view(request):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_address = None

    form = ShippingAddressForm(instance=shipping_address)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('account:dashboard')

    context = {
        'form': form,
    }
    return render(request, 'payment/shipping.html', context)


def checkout_view(request):
    """
    Renders the checkout page. If the user is authenticated and has a shipping address,
    it displays the checkout form with the user's shipping information. Otherwise, it
    renders the checkout page without pre-filled shipping details.

    Args:
        request (HttpRequest): The request object containing user and session details.

    Returns:
        HttpResponse: The rendered checkout page with or without shipping details.
    """

    if request.user.is_authenticated:
        shipping_address = get_object_or_404(ShippingAddress, user=request.user)
        if shipping_address:
            return render(request, 'payment/checkout.html', {'shipping_address': shipping_address})
    return render(request, 'payment/checkout.html')


def complete_order_view(request):
    if request.POST.get('action') == 'payment':
        name = request.POST.get('name')
        email = request.POST.get('email')
        country = request.POST.get('country')
        city = request.POST.get('city')
        street = request.POST.get('street')
        apartment = request.POST.get('apartment')
        zip = request.POST.get('zip')

        cart = Cart(request)
        total_price = cart.get_total_price()

        shipping_address, _ = ShippingAddress.objects.get_or_create(
            user=request.user,
            defaults={
                'full_name': name,
                'email': email,
                'country': country,
                'city': city,
                'street': street,
                'apartment': apartment,
                'zip': zip
            }
        )

        if request.user.is_authenticated:
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                amount=total_price
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price'],
                    user=request.user
                )
        else:
            order = Order.objects.create(
                shipping_address=shipping_address,
                amount=total_price
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price'],
                )
        return JsonResponse({'success': True})


def payment_success_view(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'payment/payment-success.html')


def payment_fail_view(request):
    return render(request, 'payment/payment-fail.html')

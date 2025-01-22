from decimal import Decimal
import uuid
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint

import stripe
from yookassa import Configuration, Payment

from cart.cart import Cart

from .forms import ShippingAddressForm
from .models import ShippingAddress, Order, OrderItem

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


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
    return render(request, 'shipping/shipping.html', context)


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
        shipping_address = get_object_or_404(
            ShippingAddress, user=request.user)
        if shipping_address:
            return render(request, 'payment/checkout.html', {'shipping_address': shipping_address})
    return render(request, 'payment/checkout.html')


def complete_order_view(request):
    if request.method == 'POST':
        payment_type = request.POST.get('stripe-payment', 'yookassa-payment')
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

        match payment_type:
            case 'stripe-payment':
                
                session_data = {
                    'mode': 'payment',
                    'success_url': request.build_absolute_uri(reverse('payment:payment-success')),
                    'cancel_url': request.build_absolute_uri(reverse('payment:payment-fail')),
                    'line_items': []
                }

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
                        session_data['line_items'].append({
                            'price_data': {
                                'unit_amount': int(item['price'] * Decimal(100)),
                                'currency': 'usd',
                                'product_data': {
                                    'name': item['product'].name,
                                },
                            },
                            'quantity': item['qty'],
                        })

                    session_data['client_reference_id'] = order.id
                    session = stripe.checkout.Session.create(
                        **session_data)
                    return redirect(session.url, code=303)

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
                        session_data['line_items'].append({
                            'price_data': {
                                'unit_amount': int(item['price'] * Decimal(100)),
                                'currency': 'usd',
                                'product_data': {
                                    'name': item['product'].name,
                                },
                            },
                            'quantity': item['qty'],
                        })

                    session_data['client_reference_id'] = order.id
                    session = stripe.checkout.Session.create(
                        **session_data)
                    return redirect(session.url, code=303)

            case 'yookassa-payment':
                idempotence_key = uuid.uuid4().hex
                currency = 'RUB'
                description = 'Товары в корзине'
                payment = Payment.create({
                    "amount": {
                        "value": str(total_price * 102),
                        "currency": currency
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": request.build_absolute_uri(reverse('payment:payment-success')),
                        "cancel_url": request.build_absolute_uri(reverse('payment:payment-fail'))
                    },
                    "capture": True,
                    "test": True,
                    "description": description,
                }, idempotence_key)

                confirmation_url = payment.confirmation.confirmation_url

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

                    return redirect(confirmation_url)

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


def payment_success_view(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'payment/payment-success.html')


def payment_fail_view(request):
    return render(request, 'payment/payment-fail.html')

@staff_member_required
def admin_order_pdf(request, order_id):
    try:
        order = Order.objects.select_related('user', 'shipping_address').get(id=order_id)
    except Order.DoesNotExist:
        raise Http404('Order does not exist')
    html = render_to_string('payment/order/pdf/pdf_invoice.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    css_path = static('payment/css/pdf.css').lstrip('/')
    stylesheets = [weasyprint.CSS(css_path)]
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=stylesheets)
    return response
    
    
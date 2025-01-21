from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

import stripe

from yookassa import Webhook, Payment, Configuration
from yookassa.domain.common import SecurityHelper
from yookassa.domain.notification import (WebhookNotificationEventType, WebhookNotificationFactory)

from .models import Order
from .tasks import send_order_confirmation


@require_POST
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WH_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        if session['mode'] == 'payment' and session['payment_status'] == 'paid':
            try:
                order_id = session['client_reference_id']
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            
            send_order_confirmation.delay(order_id)
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.save()

    return HttpResponse(status=200)


@require_POST
@csrf_exempt
def yookassa_webhook(request):
    """
    Handles incoming POST requests for Yookassa webhooks, specifically
    processing payment success notifications.

    Args:
        request (HttpRequest): The incoming HTTP request containing the 
        webhook payload and headers.

    Returns:
        HttpResponse: An HTTP response with status code 200 if the payment
        succeeded event is processed successfully, otherwise returns 400 
        for other cases.
        
    too simple
    """

    webhhook = Webhook(request.body, request.headers['Content-Type'])
    event = webhhook.parse()
    
    if event.type == 'payment.succeeded':
        return HttpResponse(status=200)

    return HttpResponse(status=400)
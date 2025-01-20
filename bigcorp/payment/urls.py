from django.urls import path

from . import views
from .webhooks import stripe_webhook, yookassa_webhook

app_name = 'payment'

urlpatterns = [
    path('shipping/', views.shipping_view, name='shipping'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('complete-order/', views.complete_order_view, name='complete-order'),
    path('payment-success/', views.payment_success_view, name='payment-success'),
    path('payment-fail/', views.payment_fail_view, name='payment-fail'),
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),
    path('yookassa-webhook/', yookassa_webhook, name='yookassa-webhook'),
]
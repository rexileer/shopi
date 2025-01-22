from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

from shop.models import Product

User = get_user_model()


class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(("email address"), max_length=254)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    apartment = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"
        ordering = ["-id"]

    def __str__(self):
        return "ShippingAddress" + " - " + self.full_name

    def get_absolute_url(self):
        return f"/payment/shipping"
    
    @classmethod
    def create_default_shipping_address(cls, user):
        default_shipping_address = {
            "user": user,
            "full_name": "Noname",
            "email": "email@example.com",
            "country": "Country",
            "city": "City",
            "street": "Street",
            "apartment": "Apartment",
            "zip": "00000",
        }
        shipping_address = cls(**default_shipping_address)
        shipping_address.save()
        return shipping_address


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gte=0), name="amount_gte_0"
            )
        ]

    def __str__(self):
        return "Order" + str(self.id)

    def get_absolute_url(self):
        return reverse("payment:order-detail", kwargs={"pk": self.pk})
    
    def get_total_cost_before_discount(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost
    
    @property
    def get_discount(self):
        if (total_cost := self.get_total_cost_before_discount()) and self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)
    
    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, blank=True, null=True, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    
    class Meta:
        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"
        ordering = ["-id"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=0), name="price_gte_0"
            )
        ]

    def __str__(self):
        return "OrderItem" + str(self.id)

    def get_cost(self):
        return self.price * self.quantity
    
    @property
    def total_cost(self):
        return self.price * self.quantity
    
    @classmethod
    def get_total_quantity_for_product(cls, product):
        return cls.objects.filter(product=product).aggregate(total_quantity=models.Sum("quantity"))["total_quantity"] or 0
    
    @staticmethod
    def get_average_price():
        return OrderItem.objects.aggregate(average_price=models.Avg("price"))["average_price"]
    
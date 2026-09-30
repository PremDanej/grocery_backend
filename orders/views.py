from decimal import Decimal
from rest_framework.exceptions import ValidationError
from .models import UserAddress, CartItem, OrderItem, Order
from .serializers import (
    UserAddressSerializer,
    CartItemSerializer,
    OrderSerializer,
)
from rest_framework import viewsets, permissions
from django.db import transaction


# Create your views here.
class UserAddressViewSet(viewsets.ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            "items__product", "address"
        )

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        cart_items = CartItem.objects.filter(user=user).select_related("product")

        if not cart_items.exists():
            raise ValidationError({"error": "Cart is empty!"})

        # To prevent tamering, Do serverside calculation
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        delivery_fee = Decimal("1.00")
        total_amount = subtotal + delivery_fee

        order = serializer.save(
            user=user,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total_amount=total_amount,
            status="PENDING",
        )

        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_locked=item.product.price,
            )
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)

        # Empty cart on successful order
        cart_items.delete()

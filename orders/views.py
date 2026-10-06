from decimal import Decimal
from typing import cast
from users.models import UserProfile
from rest_framework.exceptions import ValidationError
from users.permissions import IsAdminRole, IsOwner
from .models import UserAddress, CartItem, OrderItem, Order
from .serializers import (
    AdminOrderUpdateSerializer,
    UserAddressSerializer,
    CartItemSerializer,
    OrderSerializer,
)
from rest_framework import serializers, viewsets, permissions
from django.db import transaction


class UserAddressViewSet(viewsets.ModelViewSet):
    serializer_class = cast(type[serializers.BaseSerializer], UserAddressSerializer)
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = cast(type[serializers.BaseSerializer], CartItemSerializer)
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = cast(type[serializers.BaseSerializer], OrderSerializer)
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = cast(UserProfile, self.request.user)
        if user.is_admin:
            return Order.objects.all().prefetch_related("items__product", "address")
        return Order.objects.filter(user=user).prefetch_related(
            "items__product", "address"
        )

    def get_permissions(self):
        # Restrict updates and delete to Admins
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminRole()]
        return super().get_permissions()

    def get_serializer_class(self):
        # for Admin patch requests..
        user = cast(UserProfile, self.request.user)
        if self.action in ["update", "partial_update"] and user.is_admin:
            return cast(type[serializers.BaseSerializer], AdminOrderUpdateSerializer)
        return cast(type[serializers.BaseSerializer], OrderSerializer)

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

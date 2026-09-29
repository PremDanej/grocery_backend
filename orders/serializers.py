from rest_framework import serializers
from core.constants import CommonColumns, UserAddressColumns, RelationFields, CartItemColumns, OrderColumns, OrderItemColumns
from .models import UserAddress, CartItem, OrderItem, Order, Product
from catalog.serializers import ProductSerializer

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = [
            CommonColumns.ID,
            UserAddressColumns.LABEL,
            UserAddressColumns.FULL_ADDRESS,
            UserAddressColumns.IS_DEFAULT
        ]
        read_only_fields = [
            CommonColumns.ID
        ]

        def create(self, validated_data):
            user = self.context['request'].user
            # If the new address is set as default, unset the previous default address
            if validated_data.get(UserAddressColumns.IS_DEFAULT, False):
                UserAddress.objects.filter(user=user, is_default=True).update(is_default=False)
            return UserAddress.objects.create(user=user, **validated_data)

        def update(self, instance, validated_data):
            user = self.context['request'].user
            if validated_data.get(UserAddressColumns.IS_DEFAULT, False):
                UserAddress.objects.filter(user=user, is_default=True).exclude(id=instance.id).update(is_default=False)
            return super().update(instance, validated_data)



class CartItemSerializer(serializers.ModelSerializer):
    # Read: product details,
    # Write: To adding into cart
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)
    class Meta:
        model = CartItem
        fields = [
            CommonColumns.ID,
            RelationFields.PRODUCT,
            CartItemColumns.PRODUCT_ID,
            CartItemColumns.QUANTITY,
        ]
        read_only_fields = [CommonColumns.ID]

    def create(self, validated_data):
        user = self.context['request'].user
        product_id = validated_data.pop(CartItemColumns.PRODUCT_ID)
        quantity = validated_data.get(CartItemColumns.QUANTITY, 1)
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(
            user = user,
            product = product,
            defaults = {CartItemColumns.QUANTITY: quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            CommonColumns.ID,
            RelationFields.PRODUCT,
            OrderItemColumns.QUANTITY,
            OrderItemColumns.PRICE_LOCKED
        ]
        read_only_fields = [
            CommonColumns.ID,
            OrderItemColumns.PRICE_LOCKED
        ]


class OrderSerializer(serializers.ModelSerializer):
    # items and addresses for read only
    items = OrderItemSerializer(many=True, read_only=True)
    address = UserAddressSerializer(read_only=True)

    # For write in mobile app, we will send address_id and items as list of product_id and quantity
    address_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Order
        fields = [
            CommonColumns.ID,
            RelationFields.ADDRESS,
            OrderColumns.ADDRESS_ID,
            OrderColumns.SUBTOTAL,
            OrderColumns.DELIVERY_FEE,
            OrderColumns.DISCOUNT_AMOUNT,
            OrderColumns.TOTAL_AMOUNT,
            OrderColumns.DELIVERY_TYPE,
            OrderColumns.PAYMENT_METHOD,
            OrderColumns.STATUS,
            RelationFields.ITEMS,
            CommonColumns.CREATED_AT
        ]
        read_only_fields = [
            CommonColumns.ID,
            OrderColumns.SUBTOTAL,
            OrderColumns.TOTAL_AMOUNT,
            OrderColumns.STATUS,
            CommonColumns.CREATED_AT
        ]
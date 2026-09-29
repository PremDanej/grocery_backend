from django.db import models

# Create your models here.
import uuid
from django.contrib.auth.models import User
from core.constants import CommonColumns, OrderColumns, DatabaseTables, UserAddressColumns, CartItemColumns, OrderChoices, OrderItemColumns
from catalog.models import Product


class UserAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column=CommonColumns.ID)
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE, db_column=CommonColumns.USER_ID)
    label = models.CharField(max_length=50, db_column=UserAddressColumns.LABEL)
    full_address = models.TextField(db_column=UserAddressColumns.FULL_ADDRESS)
    is_default = models.BooleanField(default=False, db_column=UserAddressColumns.IS_DEFAULT)

    class Meta:
        db_table = DatabaseTables.USER_ADDRESS

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column=CommonColumns.ID)
    user = models.ForeignKey(User, related_name='cart_items', on_delete=models.CASCADE, db_column=CommonColumns.USER_ID)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column=CartItemColumns.PRODUCT_ID)
    quantity = models.PositiveIntegerField(default=1, db_column=CartItemColumns.QUANTITY)

    class Meta:
        db_table = DatabaseTables.CART_ITEM

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column=CommonColumns.ID)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, db_column=CommonColumns.USER_ID)
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True, db_column=OrderColumns.ADDRESS_ID)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, db_column=OrderColumns.SUBTOTAL)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, db_column=OrderColumns.DELIVERY_FEE)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, db_column=OrderColumns.DISCOUNT_AMOUNT)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, db_column=OrderColumns.TOTAL_AMOUNT)
    delivery_type = models.CharField(max_length=20, db_column=OrderColumns.DELIVERY_TYPE, choices = OrderChoices.DELIVERY_CHOICES)
    payment_method = models.CharField(max_length=20, db_column=OrderColumns.PAYMENT_METHOD, choices = OrderChoices.PAYMENT_CHOICES)
    status = models.CharField(max_length=20, db_column=OrderColumns.STATUS, choices = OrderChoices.STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, db_column=CommonColumns.CREATED_AT)

    class Meta:
        db_table = DatabaseTables.ORDER


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column=CommonColumns.ID)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, db_column=OrderItemColumns.ORDER_ID)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, db_column=OrderItemColumns.PRODUCT_ID)
    quantity = models.PositiveIntegerField(db_column=OrderItemColumns.QUANTITY)
    price_locked = models.DecimalField(max_digits=10, decimal_places=2, db_column=OrderItemColumns.PRICE_LOCKED)

    class Meta:
        db_table = DatabaseTables.ORDER_ITEM
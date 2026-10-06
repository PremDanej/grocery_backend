class DatabaseTables:
    USER_PROFILE = "user_profiles"
    CATEGORY = "categories"
    PRODUCT = "products"
    USER_ADDRESS = "user_addresses"
    CART_ITEM = "cart_items"
    ORDER = "orders"
    ORDER_ITEM = "order_items"


class CommonColumns:
    ID = "id"
    USER_ID = "user_id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class UserColumns:
    USERNAME = "username"
    EMAIL = "email"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"


class RelationFields:
    CATEGORY = "category"
    CATEGORY_NAME = "category_name"
    PRODUCT = "product"
    ADDRESS = "address"
    ITEMS = "items"


class UserRoles:
    ADMIN = "ADMIN"
    USER = "USER"
    CUSTOMER = "CUSTOMER"
    CHOICES = [
        (ADMIN, "Admin"),
        (USER, "User"),
        (CUSTOMER, "Customer"),
    ]

class ImageFolder:
    USER_FOLDER = "users/"
    CATEGORY_FOLDER = "categories/"
    PRODUCT_FOLDER = "products/"

class UserProfileColumns:
    ID = "id"
    EMAIL = "email"
    USERNAME = "username"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    PHONE_NUMBER = "phone_number"
    PROFILE_PICTURE = "profile_picture"
    ROLE = "role"
    LOYALTY_POINTS = "loyalty_points"
    MARKETING_OPT_IN = "marketing_opt_in"
    IS_ACTIVE = "is_active"
    IS_STAFF = "is_staff"


class CategoryColumns:
    NAME = "name"
    IMAGE = "image"


class ProductColumns:
    CATEGORY_ID = "category_id"
    NAME = "name"
    PRICE = "price"
    DESCRIPTION = "description"
    ORIGINAL_PRICE = "original_price"
    UNIT_SIZE = "unit_size"
    RATING_SCORE = "rating_score"
    REVIEW_COUNT = "review_count"
    IMAGE = "image"
    IS_FLASH_DEAL = "is_flash_deal"


class UserAddressColumns:
    LABEL = "label"
    FULL_ADDRESS = "full_address"
    IS_DEFAULT = "is_default"


class CartItemColumns:
    PRODUCT_ID = "product_id"
    QUANTITY = "quantity"


class OrderColumns:
    ADDRESS_ID = "address_id"
    SUBTOTAL = "subtotal"
    DELIVERY_FEE = "delivery_fee"
    DISCOUNT_AMOUNT = "discount_amount"
    TOTAL_AMOUNT = "total_amount"
    DELIVERY_TYPE = "delivery_type"
    PAYMENT_METHOD = "payment_method"
    STATUS = "status"


class OrderItemColumns:
    ORDER_ID = "order_id"
    PRODUCT_ID = "product_id"
    QUANTITY = "quantity"
    PRICE_LOCKED = "price_locked"


class OrderChoices:

    # Delivery Types
    DELIVERY_EXPRESS = "EXPRESS"
    DELIVERY_STANDARD = "STANDARD"
    DELIVERY_CHOICES = [
        (DELIVERY_EXPRESS, "Express Delivery (30-45 mins)"),
        (DELIVERY_STANDARD, "Standard Delivery (1-2 days)"),
    ]

    # Payment Methods
    PAYMENT_CASH = "CASH"
    PAYMENT_VISA = "VISA"
    PAYMENT_MASTERCARD = "MASTERCARD"
    PAYMENT_PAYPAL = "PAYPAL"
    PAYMENT_CHOICES = [
        (PAYMENT_CASH, "Cash on Delivery"),
        (PAYMENT_VISA, "Visa"),
        (PAYMENT_MASTERCARD, "MasterCard"),
        (PAYMENT_PAYPAL, "PayPal"),
    ]

    # Order Statuses
    STATUS_PENDING = "PENDING"
    STATUS_PROCESSING = "PROCESSING"
    STATUS_SHIPPED = "SHIPPED"
    STATUS_DELIVERED = "DELIVERED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_SHIPPED, "Shipped"),
        (STATUS_DELIVERED, "Delivered"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

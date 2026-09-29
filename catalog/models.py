from django.db import models

# Create your models here.
import uuid
from django.db import models
from core.constants import CommonColumns, DatabaseTables, CategoryColumns, ProductColumns

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column=CommonColumns.ID)
    name = models.CharField(max_length=100, db_column=CategoryColumns.NAME)
    image_url = models.URLField(db_column=CategoryColumns.IMAGE_URL)

    class Meta:
        db_table = DatabaseTables.CATEGORY
        verbose_name_plural = 'Categories'

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column=CommonColumns.ID)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', db_column=ProductColumns.CATEGORY_ID)
    name = models.CharField(max_length=100, db_column=ProductColumns.NAME)
    description = models.TextField(blank=True, null=True, db_column=ProductColumns.DESCRIPTION)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column=ProductColumns.PRICE)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column=ProductColumns.ORIGINAL_PRICE)
    unit_size = models.CharField(max_length=50, db_column=ProductColumns.UNIT_SIZE)
    rating_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, db_column=ProductColumns.RATING_SCORE)
    review_count = models.PositiveIntegerField(default=0, db_column=ProductColumns.REVIEW_COUNT)
    image_url = models.URLField(db_column=ProductColumns.IMAGE_URL)
    is_flash_deal = models.BooleanField(default=False, db_column=ProductColumns.IS_FLASH_DEAL)

    class Meta:
        db_table = DatabaseTables.PRODUCT
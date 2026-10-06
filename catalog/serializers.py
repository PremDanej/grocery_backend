from rest_framework import serializers
from catalog.models import Category, Product
from core.constants import CommonColumns, CategoryColumns, ProductColumns


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        # fields = '__all__'
        fields = [
            CommonColumns.ID,
            CategoryColumns.NAME,
            CategoryColumns.IMAGE
        ]

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            CommonColumns.ID,
            'category',
            ProductColumns.NAME,
            ProductColumns.DESCRIPTION,
            ProductColumns.PRICE,
            ProductColumns.ORIGINAL_PRICE,
            ProductColumns.UNIT_SIZE,
            ProductColumns.RATING_SCORE,
            ProductColumns.REVIEW_COUNT,
            ProductColumns.IMAGE,
            ProductColumns.IS_FLASH_DEAL
        ]
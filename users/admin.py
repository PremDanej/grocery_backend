from django.contrib import admin
from .models import UserProfile
from core.constants import UserProfileColumns


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        UserProfileColumns.EMAIL,
        UserProfileColumns.USERNAME,
        UserProfileColumns.ROLE,
        UserProfileColumns.LOYALTY_POINTS,
        UserProfileColumns.IS_ACTIVE,
    )
    list_filter = (
        UserProfileColumns.ROLE,
        UserProfileColumns.IS_ACTIVE,
        UserProfileColumns.MARKETING_OPT_IN,
    )
    search_fields = (
        UserProfileColumns.EMAIL,
        UserProfileColumns.USERNAME,
        UserProfileColumns.PHONE_NUMBER,
    )
    ordering = ("-created_at",)

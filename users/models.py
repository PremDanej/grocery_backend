import uuid

from django.db import models
from django.contrib.auth.models import User
from core.constants import CommonColumns, UserProfileColumns, DatabaseTables

# Create your models here.
class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column=CommonColumns.ID)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', db_column=CommonColumns.USER_ID)
    phone_number = models.CharField(max_length=15, unique=True, blank=False, null=False, db_column=UserProfileColumns.PHONE_NUMBER)
    profile_picture_url = models.URLField(blank=True, null=True, db_column=UserProfileColumns.PROFILE_PICTURE_URL)
    loyalty_points = models.PositiveIntegerField(default=0, db_column=UserProfileColumns.LOYALTY_POINTS)
    marketing_opt_in = models.BooleanField(default=False, db_column=UserProfileColumns.MARKETING_OPT_IN)
    created_at = models.DateTimeField(auto_now_add=True, db_column=CommonColumns.CREATED_AT)
    updated_at = models.DateTimeField(auto_now=True, db_column=CommonColumns.UPDATED_AT)


class Meta:
    db_table = DatabaseTables.USER_PROFILE
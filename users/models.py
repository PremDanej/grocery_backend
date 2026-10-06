import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from core.constants import CommonColumns, UserProfileColumns, DatabaseTables, UserRoles, ImageFolder


class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, password= None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault(UserProfileColumns.ROLE, UserRoles.ADMIN)
        extra_fields.setdefault(UserProfileColumns.IS_ACTIVE, True)
        extra_fields.setdefault(UserProfileColumns.IS_STAFF, True)
        return self.create_user(email, username, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column=UserProfileColumns.ID)
    email = models.EmailField(unique=True, db_column=UserProfileColumns.EMAIL)
    username = models.CharField(max_length=150, unique=True, db_column=UserProfileColumns.USERNAME)
    first_name = models.CharField(max_length=30, blank=True, db_column=UserProfileColumns.FIRST_NAME)
    last_name = models.CharField(max_length=30, blank=True, db_column=UserProfileColumns.LAST_NAME)
    phone_number = models.CharField(max_length=15, unique=True, blank=False, null=False, db_column=UserProfileColumns.PHONE_NUMBER)
    profile_picture = models.ImageField(upload_to = ImageFolder.USER_FOLDER, blank=True, null=True, db_column=UserProfileColumns.PROFILE_PICTURE)
    loyalty_points = models.PositiveIntegerField(default=0, db_column=UserProfileColumns.LOYALTY_POINTS)
    marketing_opt_in = models.BooleanField(default=False, db_column=UserProfileColumns.MARKETING_OPT_IN)
    role = models.CharField(max_length=20, choices=UserRoles.CHOICES, default=UserRoles.USER, db_column=UserProfileColumns.ROLE)
    is_active = models.BooleanField(default=True, db_column=UserProfileColumns.IS_ACTIVE)
    is_staff = models.BooleanField(default=False, db_column=UserProfileColumns.IS_STAFF)
    created_at = models.DateTimeField(auto_now_add=True, db_column=CommonColumns.CREATED_AT)
    updated_at = models.DateTimeField(auto_now=True, db_column=CommonColumns.UPDATED_AT)

    objects = UserProfileManager()
    USERNAME_FIELD = UserProfileColumns.EMAIL
    REQUIRED_FIELDS = [ UserProfileColumns.USERNAME]

    class Meta(AbstractBaseUser.Meta, PermissionsMixin.Meta):
        abstract = False
        db_table = DatabaseTables.USER_PROFILE

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN or self.is_superuser
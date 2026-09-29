from rest_framework import serializers
from .models import UserProfile
from core.constants import CommonColumns, UserColumns, UserProfileColumns


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            CommonColumns.ID,
            UserColumns.USERNAME,
            UserColumns.EMAIL,
            UserColumns.FIRST_NAME,
            UserColumns.LAST_NAME,
            UserProfileColumns.PHONE_NUMBER,
            UserProfileColumns.PROFILE_PICTURE_URL,
            UserProfileColumns.LOYALTY_POINTS,
            UserProfileColumns.MARKETING_OPT_IN,
            CommonColumns.CREATED_AT,
            CommonColumns.UPDATED_AT
        ]
        read_only_fields = [
            CommonColumns.ID,
            UserProfileColumns.LOYALTY_POINTS,
            CommonColumns.CREATED_AT,
            CommonColumns.UPDATED_AT
        ]

    def update(self, instance, validated_data):
        #update nested user fields
        user_data = validated_data.pop('user', {}) 
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        #update user profile fields
        return super().update(instance, validated_data)
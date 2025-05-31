from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from allauth.account.utils import setup_user_email

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "full_name", "password", "password2")
        extra_kwargs = {"email": {"required": True}, "full_name": {"required": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create(
            email=validated_data["email"],
            full_name=validated_data["full_name"],
            is_active=False,  # User will be activated after email verification
        )
        user.set_password(validated_data["password"])
        user.save()

        return user

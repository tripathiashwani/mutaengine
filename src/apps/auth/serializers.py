from django.core.cache import cache
from django.db import transaction
from rest_framework import serializers

from .two_fa_handlers import TwoFAHandler, OTPACTION
from .models import User


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone", "password",)
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data, is_active=False)
            return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=255, write_only=True, required=True, allow_blank=False
    )
    
    def validate(self, attrs: dict):
        email = attrs.get("email", None)
        password = attrs.get("password", None)

        if email is None or password is None:
            raise serializers.ValidationError({"msg": "email or password missing"})

        try:
            user: User = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"msg": "Invalid email or password"})

        if user.check_password(password):
            attrs["user"] = user
        else:
            attrs["user"] = None
            raise serializers.ValidationError({"msg": "Invalid email or password"})

        return attrs


class UserLogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField(
        max_length=255 * 3, required=True, allow_blank=False
    )


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = (
            "otp",
            "otp_created_at",
            "otp_tries",
            "password",
            "groups",
            "user_permissions",
            "is_deleted",
            "is_superuser",
            "is_staff",
        )


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True, allow_blank=False)

    def validate(self, attrs):
        email = attrs.get("email", None)

        if email is None:
            raise serializers.ValidationError({"msg": "Email is missing"})

        try:
            user: User = User.objects.get(email=email)
            attrs["user"] = user
        except User.DoesNotExist:
            attrs["user"] = None
            raise serializers.ValidationError(
                {"msg": "User with this email does not exist"}
            )

        return attrs


class PasswordResetVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)

    def validate(self, attrs: dict) -> dict:
        otp = attrs.get("otp", None)

        try:
            user: User = User.objects.get(email=attrs.get("email", None))
            attrs["user"] = user
        except User.DoesNotExist:
            attrs["user"] = None
            raise serializers.ValidationError("User not found")

        handler = TwoFAHandler(user=user, action=OTPACTION.RESET)
        verified, message = handler.verify_otp(otp)
        if not verified:
            raise serializers.ValidationError(message)

        cache.set(f"{user.id}_otp", otp, timeout=180)
        return super().validate(attrs)


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, allow_blank=False)
    id = serializers.CharField(required=True, allow_blank=False)
    otp = serializers.CharField(required=True, allow_blank=False)

    def validate(self, attrs: dict) -> dict:
        id = attrs.get("id", None)
        otp = attrs.get("otp", None)

        if otp is None or otp == "":
            raise serializers.ValidationError("Invalid Request")

        try:
            user: User = User.objects.get(id=id)
            attrs["user"] = user
        except User.DoesNotExist:
            attrs["user"] = None
            raise serializers.ValidationError("User not found")

        try:
            if int(cache.get(f"{user.id}_otp", None)) != int(attrs.get("otp", None)):
                raise serializers.ValidationError("Please verify otp first")
        except TypeError:
            pass

        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, allow_blank=False)
    new_password = serializers.CharField(required=True, allow_blank=False)

    def validate(self, attrs: dict) -> dict:
        current_password = attrs.get("current_password", None)
        user: User = self.context["request"].user

        if not user.check_password(current_password):
            attrs["user"] = None
            raise serializers.ValidationError("Invalid current password")
        else:
            attrs["user"] = user
        return super().validate(attrs)
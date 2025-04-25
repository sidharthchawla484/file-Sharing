from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


class ClientSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_client_user=True
        )
        
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = f'http://127.0.0.1:8000/users/verify-email/{uidb64}/{token}/'

        subject = 'Email Verification'
        message = f'Hi {user.username},\n\nPlease verify your email:\n{verification_url}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        
        return user, verification_url


class OpsSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_ops_user=True
        )

        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = f'http://127.0.0.1:8000/users/verify-email/{uidb64}/{token}/'

        subject = 'Email Verification'
        message = f'Hi {user.username},\n\nPlease verify your email:\n{verification_url}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return user, verification_url


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def validate(self, data):
        user = CustomUser.objects.filter(username=data['username']).first()
        if user and user.check_password(data['password']):
            refresh = RefreshToken.for_user(user)
            return {
                'msg': str(refresh.access_token),
                'refresh': str(refresh)
            }
        raise serializers.ValidationError('Invalid credentials')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def save(self):
        user = super().save()

        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = f'http://127.0.0.1:8000/users/verify-email/{uidb64}/{token}/'

        subject = 'Email Verification'
        message = f'Hi {user.username},\n\nPlease verify your email:\n{verification_url}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return user, verification_url

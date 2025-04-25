from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ClientSignupSerializer, OpsSignupSerializer, LoginSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from .models import CustomUser


class ClientSignupView(APIView):
    def post(self, request):
        serializer = ClientSignupSerializer(data=request.data)
        if serializer.is_valid():
            user, verification_url = serializer.save()  # get the verification URL
            return Response({"msg": f"Client registered. Check email to verify. {verification_url}"}, status=201)
        return Response(serializer.errors, status=400)


class OpsSignupView(APIView):
    def post(self, request):
        serializer = OpsSignupSerializer(data=request.data)
        if serializer.is_valid():
            user, verification_url = serializer.save()  # get the verification URL
            return Response({"msg": f"Ops user registered. Check email to verify. {verification_url}"}, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=200)
        return Response(serializer.errors, status=400)


class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({"error": "Invalid link."}, status=400)

        if default_token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            return Response({"msg": "Email verified successfully."}, status=200)
        else:
            return Response({"error": "Invalid or expired token."}, status=400)

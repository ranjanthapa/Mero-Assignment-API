import random
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from .models import UserProfile
from .serializer import UserSerializer
from .throttle import ResetPasswordRateThrottle

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


class UserView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response({"Error": "Something went wrong"}, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        user = User.objects.get(username=serializer.data["username"])
        token_obj, created = Token.objects.get_or_create(user=user)
        return Response({"message": "created successfully", "token": str(token_obj)}, status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"Error": "Please provide both username and password"}, status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"Message": "Login Success"})

        return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        login_url = request.build_absolute_uri(reverse("account:login"))
        return Response({"message": f"Logout Successfully, {login_url} for login"})


class SendPasswordResetOTP:

    @staticmethod
    def sendOTP(request, username, email, confirm_password_url):
        otp = random.randint(100000, 999999)
        template_name = 'file/reset_password_email.txt'

        context = {
            'UserName': username,
            'OTP': otp,
            "confirm_reset_password_url": confirm_password_url,
            "OrganizationName": "Mero assignment",
        }
        email_body = render_to_string(template_name, context)
        send_mail(
            subject="Password Reset OTP Confirmation",
            message='',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            html_message=email_body
        )
        request.session['otp'] = otp
        request.session.modified = True
        return otp


class PasswordResetView(APIView):
    throttle_classes = [ResetPasswordRateThrottle, ]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        if not username or not email:
            return Response({"Error": "Please provide both username and email"}, status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username, email=email).first()
        if user:
            confirm_reset_password_url = request.build_absolute_uri(reverse("account:confirm_reset_password"))
            SendPasswordResetOTP.sendOTP(request, username, email, confirm_reset_password_url)
            return Response({"message": "Check your email for OTP"}, status.HTTP_200_OK)

        return Response({"message": "Invalid Username or Email"}, status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        prover_otp = request.data.get("otp")
        username = request.data.get("username")

        user = User.objects.filter(username=username).first()
        if user and self.is_otp_valid(request, prover_otp):
            new_password = request.data.get("new_password")
            confirm_password = request.data.get("confirm_password")
            if new_password == confirm_password:
                return Response({"message": "password reset successfully"}, status.HTTP_200_OK)
            return Response({"Error": "Password do not match"}, status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def is_otp_valid(request, prover_otp):
        session_otp = request.session.get("otp")
        if session_otp == prover_otp:
            return True
        return False

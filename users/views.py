# Create your views here.
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from users.serializers import RegisterSerializer
from libs.response import APIResponse
from django.utils.crypto import get_random_string
from users.models import OTP
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterAPIView(APIView):
    """APIView to handle user registration."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return APIResponse(
                success=True,
                message="User registered successfully",
                data={
                    "email": user.email
                },
                status_code=status.HTTP_201_CREATED
            )
        return APIResponse(
            success=False,
            message="Validation error",
            data={},
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class UserProfileAPIView(APIView):
    """Get current logged-in user's profile"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return APIResponse(
            success=True,
            message="User profile fetched",
            data={
                "id": user.id,
                "email": user.email,
                "is_admin": user.is_admin,
                "is_active": user.is_active
            },
            status_code=status.HTTP_200_OK
        )


class LogoutAPIView(APIView):
    """APIView to handle user logout by invalidating the refresh token."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return APIResponse(
                success=True,
                message="Logout successful",
                data={},
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message="Logout failed",
                data={},
                status_code=status.HTTP_400_BAD_REQUEST
            )


class SendOTPAPIView(APIView):
    """APIView to send OTP to user's email."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return APIResponse(
                success=False,
                message="Email is required",
                data={},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return APIResponse(
                success=False,
                message="User not found",
                data={},
                status_code=status.HTTP_404_NOT_FOUND
            )

        raw_otp = get_random_string(length=6, allowed_chars='0123456789')
        otp_obj = OTP(user=user)
        otp_obj.set_otp(raw_otp)
        otp_obj.save()

        send_mail(
            subject="Your Login OTP",
            message=f"Your OTP is: {raw_otp}",
            from_email="jadenik13@gmail.com",
            recipient_list=[user.email],
        )

        return APIResponse(
            success=True,
            message="OTP sent to your email",
            data={},
            status_code=status.HTTP_200_OK
        )


class VerifyOTPAPIView(APIView):
    """APIView to verify the OTP sent to user's email."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(email=email)
            otp_obj = OTP.objects.filter(user=user).latest('created_at')
        except (User.DoesNotExist, OTP.DoesNotExist):
            return APIResponse(
                success=False,
                message="Invalid user or OTP",
                data={},
                status_code=status.HTTP_404_NOT_FOUND
            )

        if otp_obj.verify_otp(otp):
            refresh = RefreshToken.for_user(user)
            token_data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
            return APIResponse(
                success=True,
                message="OTP verified successfully",
                data=token_data,
                status_code=status.HTTP_200_OK
            )
        return APIResponse(
            success=False,
            message="Invalid or expired OTP",
            data={},
            status_code=status.HTTP_400_BAD_REQUEST
        )

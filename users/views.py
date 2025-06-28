# Create your views here.
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from users.serializers import RegisterSerializer
from libs.response import APIResponse
from django.utils.crypto import get_random_string
from users.models import OTP
from django.core.mail import send_mail

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


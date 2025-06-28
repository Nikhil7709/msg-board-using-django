# Create your views here.
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from users.serializers import RegisterSerializer
from libs.response import APIResponse

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


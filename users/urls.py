from django.urls import path
from users.views import (
    RegisterAPIView,
    SendOTPAPIView,
    UserProfileAPIView,
    VerifyOTPAPIView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('send-otp/', SendOTPAPIView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('logged-in-profile/', UserProfileAPIView.as_view(), name='user-profile'),
]

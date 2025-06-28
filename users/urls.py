from django.urls import path
from users.views import (
    RegisterAPIView,
    SendOTPAPIView,
    UserProfileAPIView,
    VerifyOTPAPIView,
    LogoutAPIView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('send-otp/', SendOTPAPIView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('logged-in-profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]

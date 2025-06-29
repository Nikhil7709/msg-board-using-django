from django.urls import path
from messagesapp.views import MessageDetailAPIView, MessageListCreateAPIView

urlpatterns = [
    path('', MessageListCreateAPIView.as_view(), name='message-list-create'),
    path('<int:pk>/', MessageDetailAPIView.as_view(), name='message-detail'),

]

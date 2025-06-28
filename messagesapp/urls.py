from django.urls import path
from messagesapp.views import MessageListCreateAPIView

urlpatterns = [
    path('', MessageListCreateAPIView.as_view(), name='message-list-create'),
]


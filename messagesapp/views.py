from django.shortcuts import render
from rest_framework import generics
from messagesapp.models import Message
from rest_framework import permissions
# Create your views here.
from messagesapp.serializers import MessageSerializer

class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



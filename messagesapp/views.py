from django.shortcuts import render
from rest_framework import generics
from messagesapp.models import Message
from rest_framework import permissions, status
from messagesapp.serializers import MessageSerializer
from libs.response import APIResponse


class MessageListCreateAPIView(generics.ListCreateAPIView):
    """API view to list and create messages."""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return APIResponse(
            success=True,
            message="Messages fetched successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return APIResponse(
            success=True,
            message="Message posted successfully",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


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


class MessageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete a message."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return APIResponse(
            success=True,
            message="Message fetched successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return APIResponse(
            success=True,
            message="Message updated successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return APIResponse(
            success=True,
            message="Message deleted successfully",
            data={},
            status_code=status.HTTP_204_NO_CONTENT
        )


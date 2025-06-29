from messagesapp.models import Message
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:
        model = Message
        fields = ["id", "user", "user_email", "content", "created_at"]
        read_only_fields = ["id", "user", "user_email", "created_at"]

    def create(self, validated_data):
        # Ensure the user is set from the request context
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


from django.apps import AppConfig


class MessagesappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "messagesapp"

    def ready(self):
        import messagesapp.signals

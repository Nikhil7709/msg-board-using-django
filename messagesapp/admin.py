from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from messagesapp.models import Message

@admin.register(Message)
class MessageAdmin(ImportExportModelAdmin):
    list_display = ['user', 'content', 'created_at']
    search_fields = ['user__email', 'content']
    list_filter = ['created_at']
    save_as = True


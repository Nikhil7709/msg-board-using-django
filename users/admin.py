from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from users.models import User


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ['email', 'is_admin', 'is_active']
    search_fields = ['email']
    list_filter = ['is_admin', 'is_active']
    ordering = ['-is_admin', 'email']
    save_as = True

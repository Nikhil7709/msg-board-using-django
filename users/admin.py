from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from users.models import OTP, User


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    list_display = ['email', 'is_admin', 'is_active']
    search_fields = ['email']
    list_filter = ['is_admin', 'is_active']
    ordering = ['-is_admin', 'email']
    save_as = True


@admin.register(OTP)
class OTPAdmin(ImportExportModelAdmin):
    list_display = ['user', 'created_at', 'is_valid_now']
    readonly_fields = ['created_at', 'otp_hashed']
    search_fields = ['user__email']
    list_filter = ['created_at']
    save_as = True

    def is_valid_now(self, obj):
        return obj.is_valid()
    is_valid_now.short_description = "Valid (<= 15 mins)"
    is_valid_now.boolean = True


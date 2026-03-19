from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(ModelAdmin, UserAdmin):
    list_display = ['username', 'full_name_nepali', 'role', 'post', 'email', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'full_name_nepali', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'post', 'full_name_nepali')}),
    )
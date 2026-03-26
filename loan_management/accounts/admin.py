from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(ModelAdmin, UserAdmin):
    list_display = ['username', 'full_name_nepali', 'role', 'post', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'post', 'full_name_nepali')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'post', 'full_name_nepali')}),
    )
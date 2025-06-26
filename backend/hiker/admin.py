from django.contrib import admin
from .models import User, Profile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')
    list_filter = ('is_active',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'bio', 'is_active')
    search_fields = ('user__username', 'first_name', 'last_name')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('user_id', 'email', 'first_name', 'last_name', 'role' , 'is_active')
    list_filter = ('role' , 'is_active', 'date_joined')
    search_fields = ('user_id', 'email', 'first_name', 'last_name' )
    ordering = ('user_id',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('user_id', 'role' )
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('user_id', 'role' )
        }),
    )
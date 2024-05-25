from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import EndUser, ManagerUser, Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class EndUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class ManagerUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(EndUser, EndUserAdmin)
admin.site.register(ManagerUser, ManagerUserAdmin)

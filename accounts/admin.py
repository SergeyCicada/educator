from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin-panel model profile
    """
    list_display = ('user', 'slug')
    list_display_links = ('user', 'slug')

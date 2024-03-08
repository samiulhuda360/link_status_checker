from django.contrib import admin
from rest_framework.authtoken.models import Token
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Link, LinkStatusThreshold, Index_checker_api

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('target_link', 'link_to', 'anchor_text', 'link_created', 'status_of_link')
    list_filter = ('status_of_link', 'link_created')
    search_fields = ('link_to', 'anchor_text')
    ordering = ('-link_created',)
    
admin.site.register(LinkStatusThreshold)

@admin.register(Index_checker_api)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('key',)

    def has_add_permission(self, request, obj=None):
        # Disable addition of new objects if one already exists
        return not Index_checker_api.objects.exists()
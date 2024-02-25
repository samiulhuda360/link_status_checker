from django.contrib import admin
from rest_framework.authtoken.models import Token
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Link

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('target_link', 'link_to', 'anchor_text', 'link_created', 'status_of_link')
    list_filter = ('status_of_link', 'link_created')
    search_fields = ('link_to', 'anchor_text')
    ordering = ('-link_created',)


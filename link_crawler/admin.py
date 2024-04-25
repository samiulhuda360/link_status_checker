from django.contrib import admin
from .models import Link, LinkStatusThreshold, Index_checker_api, Email_api,Domain_Blogger_Details

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('target_link', 'link_to', 'anchor_text', 'link_created', 'status_of_link')
    list_filter = ('status_of_link', 'link_created')
    search_fields = ('link_to', 'anchor_text')
    ordering = ('-link_created',)
    
    def get_changeform_initial_data(self, request):
        return {'user': request.user}
    
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)
    
admin.site.register(LinkStatusThreshold)
admin.site.register(Domain_Blogger_Details)

@admin.register(Index_checker_api)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('key',)

    def has_add_permission(self, request, obj=None):
        # Disable addition of new objects if one already exists
        return not Index_checker_api.objects.exists()
    
@admin.register(Email_api)
class Email_apiAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'sender_email', 'key')

    def has_add_permission(self, request, obj=None):
        # Disable addition of new objects if one already exists
        return not Email_api.objects.exists()
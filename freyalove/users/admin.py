from django.contrib import admin

from freyalove.users.models import Profile

# Actions

# Admin definitions
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('fb_username', 'fb_link', 'fb_id', 'fb_profile_pic')
    ordering = ('first_name',)

# Registrations
admin.site.register(Profile, ProfileAdmin)
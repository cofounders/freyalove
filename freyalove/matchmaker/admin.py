from django.contrib import admin

from freyalove.matchmaker.models import Match

# Actions

# Admin definitions
class MatchAdmin(admin.ModelAdmin):
	readonly_fields = ('success', 'rejected',)

#class MatchMakerAdmin(admin.ModelAdmin):
#	pass

# Registrations
admin.site.register(Match, MatchAdmin)
#admin.site.register(MatchMaker, MatchMakerAdmin)
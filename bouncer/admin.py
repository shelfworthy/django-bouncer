from django.contrib import admin

from .models import *
from .functions import add_invite

def send_invites(modeladmin, request, queryset):
    for waitlist in queryset.filter(date_invited=None):
        add_invite(waitlist.email)
    
send_invites.short_description = "Send invites to selected users"

class WaitListAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_added', 'date_invited')
    actions = [send_invites]

admin.site.register(WaitList, WaitListAdmin)
admin.site.register(InvitesUser)
admin.site.register(Invite)

from django.contrib import admin

from .models import *

class WaitListAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_added', 'date_invited')

admin.site.register(WaitList, WaitListAdmin)
admin.site.register(InvitesUser)
admin.site.register(Invite)

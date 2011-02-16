from django.conf import settings
from django.http import HttpResponseRedirect

class MembersOnlyMiddleware(object):
    def __init__(self):
        self.open_views = getattr(settings, 'OPEN_TO_PUBLIC_VIEWS', [])
        self.redirect_url = getattr(settings, 'MEMBERS_ONLY_REDIRECT', '/')
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated():
            return
        
        full_view_name = '%s.%s' % (view_func.__module__, view_func.__name__)
        
        if full_view_name in self.open_views:
            return
        else:
            return HttpResponseRedirect(self.redirect_url)
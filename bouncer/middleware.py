from django.conf import settings
from django.http import HttpResponseRedirect

class MembersOnlyMiddleware(object):
    def __init__(self):
        self.redirect_url = getattr(settings, 'MEMBERS_ONLY_REDIRECT', '/')

        self.exact_urls = getattr(settings, 'BOUNCER_EXACT_URLS', [])
        self.exact_urls.append(self.redirect_url)

        self.partial_urls = getattr(settings, 'BOUNCER_PARTIAL_URLS', [])

    def process_request(self, request):
        # Let Authenticated users see everything
        if request.user.is_authenticated():
            return

        # If a URL completely matches an exact url, let the user in.
        if request.path in self.exact_urls:
            return

        # If a partial is part of the URL, let the user in.
        for partial in self.partial_urls:
            if partial in request.path:
                return

        return HttpResponseRedirect(self.redirect_url)

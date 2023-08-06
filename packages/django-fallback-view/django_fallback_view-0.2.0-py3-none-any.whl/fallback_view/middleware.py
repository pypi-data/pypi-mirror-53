import re

from .utils import get_fallback_view, get_excluding_regex


class FallbackViewMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluding_regex = get_excluding_regex()
        if re.match(excluding_regex, request.path):
            try:
                FallbackView = get_fallback_view()
                view = FallbackView.as_view()
                return view(request)
            except ImportError:
                pass
        return self.get_response(request)

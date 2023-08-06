from django.conf import settings

FALLBACK_VIEW = getattr(settings, "FALLBACK_VIEW", None)



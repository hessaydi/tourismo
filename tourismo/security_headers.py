from django.conf import settings


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if "Content-Security-Policy" not in response and getattr(settings, "CONTENT_SECURITY_POLICY", ""):
            response["Content-Security-Policy"] = settings.CONTENT_SECURITY_POLICY

        if "Permissions-Policy" not in response and getattr(settings, "PERMISSIONS_POLICY", ""):
            response["Permissions-Policy"] = settings.PERMISSIONS_POLICY

        hsts_seconds = getattr(settings, "SECURE_HSTS_SECONDS", 0)
        if "Strict-Transport-Security" not in response and hsts_seconds > 0:
            hsts_value = f"max-age={hsts_seconds}"
            if getattr(settings, "SECURE_HSTS_INCLUDE_SUBDOMAINS", False):
                hsts_value += "; includeSubDomains"
            if getattr(settings, "SECURE_HSTS_PRELOAD", False):
                hsts_value += "; preload"
            response["Strict-Transport-Security"] = hsts_value

        return response

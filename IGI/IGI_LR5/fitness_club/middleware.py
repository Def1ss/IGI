from django.utils import timezone
from tzlocal import get_localzone

class ServerTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tz = get_localzone()

        request.server_now = timezone.now().astimezone(tz)
        request.server_timezone = str(tz)

        return self.get_response(request)

    def process_template_response(self, request, response):
        if hasattr(response, "context_data") and response.context_data is not None:
            response.context_data.setdefault("server_now", request.server_now)
            response.context_data.setdefault("server_timezone", request.server_timezone)

        return response
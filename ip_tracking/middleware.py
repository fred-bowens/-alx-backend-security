from django.http import HttpResponseForbidden
from .models import BlockedIP, RequestLog
from django.utils.timezone import now

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            timestamp=now()
        )

        return self.get_response(request)

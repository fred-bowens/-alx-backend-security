from django.utils.timezone import now
from django.http import HttpResponseForbidden
from django.core.cache import cache
from ipgeolocation import IpGeoLocation
from .models import RequestLog, BlockedIP

geo_locator = IpGeoLocation()

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

        cache_key = f"geo_{ip}"
        geo_info = cache.get(cache_key)

        if not geo_info:
            try:
                geo_data = geo_locator.get(ip)

                country = geo_data.get('country_name', '')
                city = geo_data.get('city', '')

                geo_info = {'country': country, 'city': city}
                cache.set(cache_key, geo_info, timeout=86400)

            except Exception as e:
                
                geo_info = {'country': '', 'city': ''}

        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            timestamp=now(),
            country=geo_info['country'],
            city=geo_info['city']
        )

        return self.get_response(request)

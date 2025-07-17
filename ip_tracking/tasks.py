from celery import shared_task
from django.utils.timezone import now, timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_ips():
    one_hour_ago = now() - timedelta(hours=1)  # 2. Look back one hour
    request_logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)  # 3. Filter recent logs

    ip_counts = {}
    flagged_ips = set()

    for log in request_logs:
        ip = log.ip_address
        ip_counts[ip] = ip_counts.get(ip, 0) + 1

        if log.path in ['/admin', '/login'] and ip not in flagged_ips:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': f"Accessed sensitive path: {log.path}"}
            )
            flagged_ips.add(ip)

    for ip, count in ip_counts.items():
        if count > 100 and ip not in flagged_ips:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': f"Made {count} requests in 1 hour"}
            )

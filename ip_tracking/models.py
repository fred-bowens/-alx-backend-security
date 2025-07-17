from django.db import models

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=200)

    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)  # 2. IP address that triggered suspicion
    reason = models.TextField()  # 3. Explanation of why this IP was flagged
    flagged_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.ip_address} - {self.path/reason} at {self.timestamp}"

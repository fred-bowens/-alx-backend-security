from django.db import models

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()  # 2. Stores IPv4 or IPv6
    timestamp = models.DateTimeField(auto_now_add=True)  # 3. Automatically saves current time
    path = models.CharField(max_length=200)  # 4. Path the user accessed

    def __str__(self):
        return f"{self.ip_address} - {self.path} at {self.timestamp}"

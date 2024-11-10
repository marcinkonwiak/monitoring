import uuid

from django.db import models


class HostStats(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    time = models.DateTimeField()
    cpu_percent = models.FloatField()
    ram_total = models.IntegerField()
    ram_available = models.IntegerField()
    ram_used = models.IntegerField()
    host_id = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    platform_version = models.CharField(max_length=255)
    processes = models.IntegerField()

import uuid
from datetime import datetime
from typing import Any

from django.db import models


class Host(models.Model):
    host_id = models.CharField(max_length=255, unique=True, primary_key=True)
    os = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.host_id


class HostStats(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="stats")
    time = models.DateTimeField()
    cpu_percent = models.FloatField()
    ram_total = models.IntegerField()
    ram_available = models.IntegerField()
    ram_used = models.IntegerField()
    os = models.CharField(max_length=255)
    platform = models.CharField(max_length=255)
    platform_version = models.CharField(max_length=255)
    processes = models.IntegerField()

    objects = models.Manager()

    @classmethod
    def from_proto_dict(cls, host: Host, data: Any) -> "HostStats":
        return cls(
            host=host,
            time=datetime.fromtimestamp(data.timestamp),
            cpu_percent=data.cpu.percent,
            ram_total=data.ram.total,
            ram_available=data.ram.available,
            ram_used=data.ram.used,
            os=data.os.os,
            platform=data.os.platform,
            platform_version=data.os.platformVersion,
            processes=data.os.processes,
        )

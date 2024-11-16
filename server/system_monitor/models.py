import uuid
from datetime import datetime
from typing import Any

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

    @classmethod
    def from_proto_dict(cls, data: Any) -> "HostStats":
        return cls(
            time=datetime.fromtimestamp(data.timestamp),
            cpu_percent=data.cpu.percent,
            ram_total=data.ram.total,
            ram_available=data.ram.available,
            ram_used=data.ram.used,
            host_id=data.os.hostID,
            os=data.os.os,
            platform=data.os.platform,
            platform_version=data.os.platformVersion,
            processes=data.os.processes,
        )

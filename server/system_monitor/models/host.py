import uuid
from datetime import UTC, datetime
from typing import Any

from django.db import models


class Host(models.Model):
    host_id = models.CharField(max_length=255, primary_key=True, unique=True)
    os = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.host_id


class HostBaseStats(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    host = models.ForeignKey(
        Host, on_delete=models.CASCADE, related_name="stats", null=True, blank=True
    )
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
    def from_proto_dict(cls, host: Host, data: Any) -> "HostBaseStats":
        return cls(
            host=host,
            time=datetime.fromtimestamp(data.timestamp, tz=UTC),
            cpu_percent=data.cpu.percent,
            ram_total=data.ram.total,
            ram_available=data.ram.available,
            ram_used=data.ram.used,
            os=data.os.os,
            platform=data.os.platform,
            platform_version=data.os.platformVersion,
            processes=data.os.processes,
        )


class HostProcesses(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    pid = models.IntegerField()
    name = models.CharField(max_length=255)
    cpu = models.FloatField()
    mem = models.FloatField()
    host = models.ForeignKey(
        Host, on_delete=models.CASCADE, related_name="processes", null=True, blank=True
    )

    class Meta:
        ordering = ("-cpu",)

    def __str__(self):
        if self.name:
            return f"{self.pid} ({self.name})"
        return self.pid

    @classmethod
    def from_proto_list(cls, host: Host, data: list) -> list["HostProcesses"]:
        return [
            cls(
                pid=process.Pid,
                name=process.Name,
                cpu=process.Cpu,
                mem=process.Mem,
                host=host,
            )
            for process in data
        ]


class HostContainers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    host = models.ForeignKey(
        Host, on_delete=models.CASCADE, related_name="containers", null=True, blank=True
    )

    @classmethod
    def from_proto_list(cls, host: Host, data: list) -> list["HostContainers"]:
        try:
            instances = [
                cls(
                    name=container.Name,
                    image=container.Image,
                    host=host,
                )
                for container in data
            ]
            print(f"HostContainers instances created: {instances}")
            return instances
        except Exception as e:
            print(f"Error in from_proto_list: {e}")
            return []

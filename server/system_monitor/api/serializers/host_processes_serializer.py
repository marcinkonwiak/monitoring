from rest_framework import serializers

from system_monitor.models.host import HostProcesses


class HostProcessesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostProcesses
        fields = ["id", "pid", "name", "cpu", "mem", "host"]

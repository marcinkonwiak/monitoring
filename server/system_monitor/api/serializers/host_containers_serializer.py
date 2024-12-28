from rest_framework import serializers

from system_monitor.models.host import HostContainers


class HostContainersSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostContainers
        fields = ["id", "name", "image", "host"]

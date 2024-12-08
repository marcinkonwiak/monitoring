from django_socio_grpc import proto_serializers
from rest_framework import serializers


class StatsCpuInputSerializer(proto_serializers.ProtoSerializer):
    percent = serializers.FloatField()


class StatsRamInputSerializer(proto_serializers.BaseProtoSerializer):
    total = serializers.IntegerField()
    available = serializers.IntegerField()
    used = serializers.IntegerField()

    def to_proto_message(self):
        return [
            {"name": "total", "type": "uint64"},
            {"name": "available", "type": "uint64"},
            {"name": "used", "type": "uint64"},
        ]


class StatsOsInputSerializer(proto_serializers.BaseProtoSerializer):
    hostID = serializers.CharField(max_length=255)
    os = serializers.CharField(max_length=255)
    platform = serializers.CharField(max_length=255)
    platformVersion = serializers.CharField(max_length=255)
    processes = serializers.IntegerField()

    def to_proto_message(self):
        return [
            {"name": "hostID", "type": "string"},
            {"name": "os", "type": "string"},
            {"name": "platform", "type": "string"},
            {"name": "platformVersion", "type": "string"},
            {"name": "processes", "type": "uint64"},
        ]


class ProcessInputSerializer(proto_serializers.BaseProtoSerializer):
    Pid = serializers.IntegerField()
    Name = serializers.CharField()
    Cpu = serializers.FloatField()
    Mem = serializers.FloatField()

    def to_proto_message(self):
        return [
            {"name": "Pid", "type": "int32"},
            {"name": "Name", "type": "string"},
            {"name": "Cpu", "type": "float"},
            {"name": "Mem", "type": "float"},
        ]


class ContainerInputSerializer(proto_serializers.BaseProtoSerializer):
    ID = serializers.CharField()
    Name = serializers.CharField()
    Image = serializers.CharField()

    def to_proto_message(self):
        return [
            {"name": "ID", "type": "string"},
            {"name": "Name", "type": "string"},
            {"name": "Image", "type": "string"},
        ]


class StatsDataInputSerializer(proto_serializers.ProtoSerializer):
    timestamp = serializers.IntegerField()
    cpu = StatsCpuInputSerializer()
    ram = StatsRamInputSerializer()
    os = StatsOsInputSerializer()
    processes = serializers.ListField(child=ProcessInputSerializer())
    containers = serializers.ListField(child=ContainerInputSerializer())

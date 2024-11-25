import asyncio
from datetime import datetime

from asgiref.sync import sync_to_async
from django_socio_grpc.decorators import grpc_action
from django_socio_grpc.generics import GenericService

from .models import HostStats, Host
from .serializers import StatsDataInputSerializer


class HostStatsService(GenericService):
    serializer_class = StatsDataInputSerializer

    @grpc_action(
        request=StatsDataInputSerializer,
        response=None,
        request_stream=True,
        response_stream=True,
    )
    async def Stream(self, request, context):
        lock = asyncio.Lock()
        elements: list[HostStats] = []

        async for stats_data in request:
            host_id = stats_data.os.hostID

            host, created = await sync_to_async(Host.objects.get_or_create)(
                host_id=host_id
            )

            host.last_seen = datetime.now()
            host.os = stats_data.os.os
            await sync_to_async(host.save)()

            host_stats = HostStats.from_proto_dict(host, stats_data)

            async with lock:
                elements.append(host_stats)

                if len(elements) == 10:
                    await sync_to_async(HostStats.objects.bulk_create)(elements)
                    elements.clear()

        if elements:
            await sync_to_async(HostStats.objects.bulk_create)(elements)

        return

import asyncio
from datetime import UTC, datetime

from django_socio_grpc.decorators import grpc_action
from django_socio_grpc.generics import GenericService
from django_socio_grpc.request_transformer.grpc_internal_proxy import (
    GRPCInternalProxyContext,
)
from grpc._cython.cygrpc import _MessageReceiver  # noqa F401

from .models import Host, HostStats
from .serializers import StatsDataInputSerializer


class HostStatsService(GenericService):
    serializer_class = StatsDataInputSerializer

    @grpc_action(
        request=StatsDataInputSerializer,
        response=None,
        request_stream=True,
        response_stream=True,
    )
    async def Stream(
        self, request: _MessageReceiver, context: GRPCInternalProxyContext
    ) -> None:
        lock = asyncio.Lock()
        elements: list[HostStats] = []

        async for stats_data in request:
            stats_data: StatsDataInputSerializer
            host_id = stats_data.os.hostID

            host, _ = await Host.objects.aget_or_create(host_id=host_id)
            host.last_seen = datetime.now(tz=UTC)
            host.os = stats_data.os.os
            await host.asave()

            host_stats = HostStats.from_proto_dict(host, stats_data)

            async with lock:
                elements.append(host_stats)
                if len(elements) == 10:
                    await HostStats.objects.abulk_create(elements)
                    elements.clear()

        if elements:
            await HostStats.objects.bulk_create(elements)

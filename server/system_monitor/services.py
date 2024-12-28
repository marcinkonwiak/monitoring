import asyncio
from datetime import UTC, datetime

from asgiref.sync import sync_to_async
from django.db import transaction
from django_socio_grpc.decorators import grpc_action
from django_socio_grpc.generics import GenericService
from django_socio_grpc.request_transformer.grpc_internal_proxy import (
    GRPCInternalProxyContext,
)
from grpc._cython.cygrpc import _MessageReceiver  # noqa F401

from .models import Host, HostBaseStats
from .models.host import HostContainers, HostProcesses
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
        base_stats: list[HostBaseStats] = []
        processes: list[HostProcesses] = []
        containers: list[HostContainers] = []

        async def save_data():
            async with lock:
                if base_stats:
                    print(f"Saving {len(base_stats)} HostBaseStats")
                    await HostBaseStats.objects.abulk_create(base_stats)
                    base_stats.clear()

                if processes:
                    print(f"Saving {len(processes)} HostProcesses")
                    await HostProcesses.objects.abulk_create(processes)
                    processes.clear()

                if containers:
                    print(f"Saving {len(containers)} HostContainers")
                    await HostContainers.objects.abulk_create(containers)
                    containers.clear()

        async def delete_existing_data(host):
            def sync_delete():
                with transaction.atomic():
                    HostProcesses.objects.filter(host=host).delete()
                    HostContainers.objects.filter(host=host).delete()

            await sync_to_async(sync_delete)()

        try:
            async for stats_data in request:
                try:
                    stats_data: StatsDataInputSerializer
                    host_id = stats_data.os.hostID

                    host, _ = await Host.objects.aget_or_create(host_id=host_id)
                    host.last_seen = datetime.now(tz=UTC)
                    host.os = stats_data.os.os
                    await host.asave()

                    await delete_existing_data(host)

                    host_base_stats = HostBaseStats.from_proto_dict(host, stats_data)
                    if host_base_stats:
                        base_stats.append(host_base_stats)
                    else:
                        print("Warning: HostBaseStats is None or invalid")

                    new_processes = HostProcesses.from_proto_list(
                        host, stats_data.processes
                    )
                    if new_processes:
                        processes.extend(new_processes)
                    else:
                        print("Warning: HostProcesses is empty or invalid")

                    new_containers = HostContainers.from_proto_list(
                        host, stats_data.containers
                    )
                    if new_containers:
                        containers.extend(new_containers)
                    else:
                        print("Warning: HostContainers is empty or invalid")

                    if (
                        len(base_stats) >= 100
                        or len(processes) >= 100
                        or len(containers) >= 100
                    ):
                        await save_data()

                except Exception as e:
                    print(f"Exception while processing stats data: {e}")

            print("Saving remaining data...")
            await save_data()

        except Exception as e:
            print(f"Exception in Stream: {e}")

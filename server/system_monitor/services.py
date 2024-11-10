from django_socio_grpc.decorators import grpc_action
from django_socio_grpc.generics import GenericService

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
        async for stats_data in request:
            print("🐣 Received data:")
            print(stats_data)

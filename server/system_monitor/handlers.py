from django_socio_grpc.services.app_handler_registry import AppHandlerRegistry

from .services import HostStatsService


def grpc_handlers(server):
    app_registry = AppHandlerRegistry("system_monitor", server)
    app_registry.register(HostStatsService)

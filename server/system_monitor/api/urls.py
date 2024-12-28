from django.urls import path

from .views import HostContainersView, HostProcessesView, HostStatsDataView

urlpatterns = [
    path("host-processes/", HostProcessesView.as_view(), name="host_processes"),
    path("host-containers/", HostContainersView.as_view(), name="host_processes"),
    path(
        "host/<str:host_id>/stats-data/",
        HostStatsDataView.as_view(),
        name="host_stats_data",
    ),
]

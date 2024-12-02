from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, View

from system_monitor.models import Host


class HostDetailView(DetailView):
    model = Host
    template_name = "host_detail.html"
    context_object_name = "host"

    def get_object(self):
        host_id = self.kwargs.get("host_id")
        return get_object_or_404(Host, host_id=host_id)


class HostStatsDataView(View):
    def get(self, request, host_id):
        host = get_object_or_404(Host, host_id=host_id)
        stats = host.stats.order_by("time")
        stats_data = list(stats.values())
        return JsonResponse({"stats": stats_data})

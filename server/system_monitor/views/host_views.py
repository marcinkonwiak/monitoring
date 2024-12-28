from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, View

from system_monitor.models import Host


class HostDetailView(DetailView):
    model = Host
    template_name = "host_detail.html"
    context_object_name = "host"

    def get_object(self, queryset=None):
        host_id = self.kwargs.get("host_id")
        return get_object_or_404(Host, host_id=host_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        host = self.get_object()

        context["base_stats"] = host.stats.order_by("-time").first()
        total_processes = host.processes.count()
        context["total_processes"] = total_processes
        latest_stats = host.stats.order_by("-time").first()
        if latest_stats:
            context["platform"] = latest_stats.platform
            context["platform_version"] = latest_stats.platform_version
            context["cpu_percent"] = latest_stats.cpu_percent
        else:
            context["platform"] = "Unknown"
            context["platform_version"] = "Unknown"
            context["cpu_percent"] = 0

        return context


class HostListView(View):
    def get(self, request, *args, **kwargs):
        hosts = Host.objects.all()
        return render(request, "host_list_view.html", {"hosts": hosts})

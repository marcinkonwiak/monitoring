from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from system_monitor.models import Host


class HostStatsDataView(View):
    def get(self, request, host_id):
        host = get_object_or_404(Host, host_id=host_id)

        try:
            limit = int(request.GET.get("limit", 0))
            if limit < 0:
                return JsonResponse({"error": "Invalid limit value."}, status=400)
        except ValueError:
            return JsonResponse({"error": "Limit must be an integer."}, status=400)

        stats_data = host.stats.order_by("-time").values()
        if limit:
            stats_data = stats_data[:limit]

        return JsonResponse({"stats": list(stats_data)})

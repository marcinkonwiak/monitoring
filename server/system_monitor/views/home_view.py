from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from system_monitor.models import Host


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hosts"] = Host.objects.all()
        context["host_count"] = Host.objects.count()

        return context

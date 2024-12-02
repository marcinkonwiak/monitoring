from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
from .views.host_views import HostDetailView, HostStatsDataView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", views.BaseLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", views.HomeView.as_view(), name="home"),
    path("host/", views.HomeView.as_view(), name="hosts"),
    path("host/<str:host_id>/", HostDetailView.as_view(), name="host_detail"),
    path(
        "host/<str:host_id>/stats-data/",
        HostStatsDataView.as_view(),
        name="host_stats_data",
    ),
]

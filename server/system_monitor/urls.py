from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from . import views
from .views.host_views import HostDetailView, HostListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", views.BaseLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", views.HomeView.as_view(), name="home"),
    path("host/", HostListView.as_view(), name="hosts"),
    path("host/<str:host_id>/", HostDetailView.as_view(), name="host_detail"),
    path("api/", include("system_monitor.api.urls")),
]

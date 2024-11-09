from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/login/', views.BaseLoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("", views.HomeView.as_view(), name="home"),
    # path("instances/", views.HomeView.as_view(), name="instances"),
]

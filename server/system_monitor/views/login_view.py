from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class BaseLoginView(LoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

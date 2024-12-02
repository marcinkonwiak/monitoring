from .models import Host


def hosts(request):
    return {"hosts": Host.objects.all()}

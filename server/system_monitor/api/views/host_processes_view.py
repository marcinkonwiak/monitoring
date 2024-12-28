from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from system_monitor.api.serializers import HostProcessesSerializer
from system_monitor.models.host import HostProcesses


class HostProcessesView(APIView):
    def get(self, request):
        host_id = request.query_params.get("host_id")
        name_query = request.query_params.get("name", "")

        if not host_id:
            return Response(
                {"error": "host_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        processes = HostProcesses.objects.filter(host__host_id=host_id)
        if name_query:
            processes = processes.filter(name__icontains=name_query)

        processes.order_by("-cpu")

        serializer = HostProcessesSerializer(processes, many=True)
        return Response(serializer.data)

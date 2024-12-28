from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from system_monitor.api.serializers import HostContainersSerializer
from system_monitor.models.host import HostContainers


class HostContainersView(APIView):
    def get(self, request):
        host_id = request.query_params.get("host_id")
        name_query = request.query_params.get("name", "")

        if not host_id:
            return Response(
                {"error": "host_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        containers = HostContainers.objects.filter(host__host_id=host_id)
        if name_query:
            containers = containers.filter(name__icontains=name_query)

        if not containers.exists():
            return Response(
                {"message": "No containers found"}, status=status.HTTP_200_OK
            )

        serializer = HostContainersSerializer(containers, many=True)
        return Response(serializer.data)

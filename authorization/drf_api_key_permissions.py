# Python.DjangorestframeworkApiKey.json -> "Django REST Framework API Key Python" [Authorization]
# Expected: import rest_framework_api_key; method get_from_key
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey


class ReportsView(APIView):
    permission_classes = [HasAPIKey]

    def get(self, request):
        key = request.META["HTTP_AUTHORIZATION"].split()[1]
        api_key = APIKey.objects.get_from_key(key)
        return Response({"caller": api_key.name})

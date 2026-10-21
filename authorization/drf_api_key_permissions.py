# Python.DjangorestframeworkApiKey.json -> "Django REST Framework API Key Python" [Authorization]
# Expected: import rest_framework_api_key; method get_from_key
# Partner integration endpoints; partners call with "Authorization: Api-Key <key>".
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey, KeyParser


class PartnerAPIView(APIView):
    permission_classes = [HasAPIKey]
    key_parser = KeyParser()

    def get_api_key(self, request) -> APIKey:
        return APIKey.objects.get_from_key(self.key_parser.get(request))


class PartnerKeyInfoView(PartnerAPIView):
    def get(self, request):
        api_key = self.get_api_key(request)
        return Response({"partner": api_key.name, "created": api_key.created, "expires": api_key.expiry_date})


class PartnerPingView(PartnerAPIView):
    def post(self, request):
        return Response({"partner": self.get_api_key(request).name, "status": "ok"})

# Python.DjangoAllauth.json -> "Django Allauth Python" [Authentication]
# Expected: import allauth.headless.contrib.rest_framework.authentication
# DRF endpoints for a SPA that signs in through allauth headless and sends the X-Session-Token header.
from allauth.headless.contrib.rest_framework.authentication import XSessionTokenAuthentication
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(max_length=150, allow_blank=True)
    last_name = serializers.CharField(max_length=150, allow_blank=True)


class ProfileView(APIView):
    authentication_classes = [XSessionTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ProfileSerializer(request.user).data)

    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        for field, value in serializer.validated_data.items():
            setattr(request.user, field, value)
        request.user.save(update_fields=list(serializer.validated_data))
        return Response(ProfileSerializer(request.user).data)

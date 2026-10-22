# Python.DjangoInputValidation.json -> "Django Input Validation Python" [InputValidation]
# Expected: method rest_framework is_valid (DRF serializer validation)
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class OrderLineSerializer(serializers.Serializer):
    sku = serializers.RegexField(regex=r"^[A-Z0-9-]{4,20}$")
    quantity = serializers.IntegerField(min_value=1, max_value=100)


class CreateOrderSerializer(serializers.Serializer):
    lines = OrderLineSerializer(many=True, allow_empty=False)
    coupon = serializers.CharField(required=False, max_length=32)

    def validate_coupon(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("coupon codes are alphanumeric")
        return value.upper()


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"lines": len(serializer.validated_data["lines"])}, status=status.HTTP_201_CREATED)

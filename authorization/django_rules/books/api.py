# Python.DjangoRules.json -> "Django Rules Python" [Authorization]
# Expected: import rules.contrib.rest_framework
from rest_framework import serializers, viewsets
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = ("id", "title", "summary", "author", "published_at")
        read_only_fields = ("published_at",)


class BookViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author")
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

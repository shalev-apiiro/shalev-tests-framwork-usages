# Python.DjangoRules.json -> "Django Rules Python" [Authorization]
# Expected: import rules.contrib.admin
from django.contrib import admin
from rules.contrib.admin import ObjectPermissionsModelAdmin

from .models import Book


@admin.register(Book)
class BookAdmin(ObjectPermissionsModelAdmin):
    list_display = ("title", "author", "published_at")
    list_filter = ("published_at",)
    search_fields = ("title", "author__username")

# Python.StrawberryGraphqlDjangoPermissions.json -> "Strawberry Django Permissions Python" [Authorization]
# Expected: none (model only; schema.py carries the matches)
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    published = models.BooleanField(default=False)
    internal_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["title"]
        permissions = [("view_internal_notes", "Can view internal editorial notes")]

    def __str__(self):
        return self.title

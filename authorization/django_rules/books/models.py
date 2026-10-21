# Python.DjangoRules.json -> "Django Rules Python" [Authorization]
# Expected: import rules.contrib.models
import rules
from django.conf import settings
from django.db import models
from django.urls import reverse
from rules.contrib.models import RulesModel

from .predicates import is_book_author, is_editor


class Book(RulesModel):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="books")
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["title"]
        rules_permissions = {
            "add": rules.is_authenticated,
            "view": rules.always_allow,
            "change": is_book_author | is_editor,
            "delete": is_book_author,
            "publish": is_editor,
        }

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("books:detail", kwargs={"pk": self.pk})

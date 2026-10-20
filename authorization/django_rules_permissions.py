# Python.DjangoRules.json -> "Django Rules Python" [Authorization]
# Expected: imports rules.contrib.views / rest_framework / models / admin;
#           methods rules.has_perm + rules.test_rule; decorator permission_required
import rules
from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from rest_framework import viewsets
from rules.contrib.admin import ObjectPermissionsModelAdmin
from rules.contrib.models import RulesModel
from rules.contrib.rest_framework import AutoPermissionViewSetMixin
from rules.contrib.views import PermissionRequiredMixin, objectgetter, permission_required


@rules.predicate
def is_author(user, book):
    return book.author == user


rules.add_rule("is_author", is_author)
rules.add_perm("books.change_book", is_author)


class Book(RulesModel):
    title = models.CharField(max_length=100)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    class Meta:
        rules_permissions = {"change": is_author, "delete": is_author}


@admin.register(Book)
class BookAdmin(ObjectPermissionsModelAdmin):
    pass


class BookViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all()


class BookEditView(PermissionRequiredMixin):
    permission_required = "books.change_book"


@permission_required("books.change_book", fn=objectgetter(Book, "book_id"))
def edit_book(request, book_id):
    return HttpResponse("edited")


def can_edit(user, book):
    return rules.has_perm("books.change_book", user, book) and rules.test_rule("is_author", user, book)

# Python.StrawberryGraphqlDjangoPermissions.json -> "Strawberry Django Permissions Python" [Authorization]
# Expected: import strawberry_django.permissions; methods HasPerm, HasSourcePerm, HasRetvalPerm,
#           IsStaff, IsSuperuser
import strawberry
import strawberry_django
from strawberry_django.permissions import (
    HasPerm,
    HasRetvalPerm,
    HasSourcePerm,
    IsAuthenticated,
    IsStaff,
    IsSuperuser,
)

from .models import Book


@strawberry_django.type(Book)
class BookType:
    title: strawberry.auto

    @strawberry_django.field(extensions=[HasSourcePerm("books.view_book")])
    def secret_notes(self, root: Book) -> str:
        return root.notes


@strawberry.type
class Query:
    books: list[BookType] = strawberry_django.field(extensions=[IsAuthenticated(), HasRetvalPerm("books.view_book")])
    drafts: list[BookType] = strawberry_django.field(extensions=[HasPerm("books.view_draft")])
    staff_books: list[BookType] = strawberry_django.field(extensions=[IsStaff()])
    all_books: list[BookType] = strawberry_django.field(extensions=[IsSuperuser()])


schema = strawberry.Schema(query=Query)

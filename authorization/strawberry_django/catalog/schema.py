# Python.StrawberryGraphqlDjangoPermissions.json -> "Strawberry Django Permissions Python" [Authorization]
# Expected: import strawberry_django.permissions; method IsStaff (resolver decorator). HasPerm, HasSourcePerm,
#           HasRetvalPerm and IsSuperuser sit in class-body field assignments, which the matcher does not scan.
import strawberry
import strawberry_django
from django.contrib.auth import get_user_model
from strawberry_django.optimizer import DjangoOptimizerExtension
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
    id: strawberry.auto
    title: strawberry.auto
    isbn: strawberry.auto
    published: strawberry.auto
    internal_notes: str | None = strawberry_django.field(extensions=[HasSourcePerm("catalog.view_internal_notes")])


@strawberry_django.type(get_user_model())
class UserType:
    id: strawberry.auto
    username: strawberry.auto
    email: strawberry.auto


@strawberry_django.input(Book)
class BookInput:
    title: strawberry.auto
    isbn: strawberry.auto


@strawberry.type
class Query:
    books: list[BookType] = strawberry_django.field(extensions=[IsAuthenticated()])
    book: BookType | None = strawberry_django.field(extensions=[HasRetvalPerm("catalog.view_book")])
    users: list[UserType] = strawberry_django.field(extensions=[IsSuperuser()])

    @strawberry_django.field(extensions=[IsStaff()])
    def unpublished_books(self) -> list[BookType]:
        return Book.objects.filter(published=False)


@strawberry.type
class Mutation:
    create_book: BookType = strawberry_django.mutations.create(BookInput, extensions=[HasPerm("catalog.add_book")])


schema = strawberry.Schema(query=Query, mutation=Mutation, extensions=[DjangoOptimizerExtension])

# Python.StrawberryPermissions.json -> "Strawberry Permissions Python" [Authorization]
# Expected: imports strawberry.permission + strawberry.BasePermission; method PermissionExtension
# Schema served by strawberry.django.views.AsyncGraphQLView, so info.context.request is the Django request.
import typing

import strawberry
from strawberry import BasePermission
from strawberry.permission import PermissionExtension
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = "Authentication required"
    error_extensions = {"code": "UNAUTHENTICATED"}

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        return info.context.request.user.is_authenticated


class IsOrganizationAdmin(BasePermission):
    message = "Organization admins only"
    error_extensions = {"code": "FORBIDDEN"}

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        user = info.context.request.user
        return user.is_authenticated and user.memberships.filter(role="admin").exists()


@strawberry.type
class Member:
    username: str
    email: str
    role: str


@strawberry.type
class Query:
    @strawberry.field(extensions=[PermissionExtension(permissions=[IsAuthenticated()])])
    def me(self, info: Info) -> Member:
        user = info.context.request.user
        return Member(username=user.username, email=user.email, role=user.memberships.first().role)

    @strawberry.field(extensions=[PermissionExtension(permissions=[IsOrganizationAdmin()], fail_silently=True)])
    def members(self, info: Info) -> list[Member]:
        organization = info.context.request.user.memberships.first().organization
        return [
            Member(username=m.user.username, email=m.user.email, role=m.role)
            for m in organization.memberships.select_related("user")
        ]


schema = strawberry.Schema(query=Query)

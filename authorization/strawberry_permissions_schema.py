# Python.StrawberryPermissions.json -> "Strawberry Permissions Python" [Authorization]
# Expected: imports strawberry.permission + strawberry.BasePermission; method PermissionExtension
import typing

import strawberry
from strawberry import BasePermission
from strawberry.permission import PermissionExtension
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        return info.context["request"].user.is_authenticated


class IsAdmin(BasePermission):
    message = "Admins only"

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        return info.context["request"].user.is_staff


@strawberry.type
class Query:
    @strawberry.field(extensions=[PermissionExtension(permissions=[IsAuthenticated()])])
    def me(self, info: Info) -> str:
        return info.context["request"].user.username

    @strawberry.field(extensions=[PermissionExtension(permissions=[IsAdmin()], fail_silently=True)])
    def audit_log(self) -> list[str]:
        return ["login"]


schema = strawberry.Schema(query=Query)

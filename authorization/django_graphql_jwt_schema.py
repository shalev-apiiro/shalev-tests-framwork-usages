# Python.DjangoGraphqlJwt.json -> "Django Graphql JWT Python" [Authorization]
# Expected: decorators graphql_jwt permission_required, staff_member_required, superuser_required
import graphene
import graphql_jwt
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required, permission_required, staff_member_required, superuser_required


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "is_active", "is_staff", "date_joined")


class LogEntryType(DjangoObjectType):
    class Meta:
        model = LogEntry
        fields = ("id", "action_time", "user", "object_repr", "change_message")


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType, active=graphene.Boolean())
    admin_log = graphene.List(LogEntryType, limit=graphene.Int(default_value=50))

    @login_required
    def resolve_me(self, info):
        return info.context.user

    @staff_member_required
    def resolve_users(self, info, active=None):
        users = get_user_model().objects.order_by("username")
        return users if active is None else users.filter(is_active=active)

    @permission_required("admin.view_logentry")
    def resolve_admin_log(self, info, limit):
        return LogEntry.objects.select_related("user").order_by("-action_time")[:limit]


class DeactivateUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    user = graphene.Field(UserType)

    @superuser_required
    def mutate(self, info, user_id):
        user = get_user_model().objects.get(pk=user_id)
        user.is_active = False
        user.save(update_fields=["is_active"])
        return DeactivateUser(user=user)


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    deactivate_user = DeactivateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

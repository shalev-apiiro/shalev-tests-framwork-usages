# Python.DjangoGraphqlJwt.json -> "Django Graphql JWT Python" [Authorization]
# Expected: decorators graphql_jwt permission_required, staff_member_required, superuser_required
import graphene
from graphql_jwt.decorators import permission_required, staff_member_required, superuser_required


class Query(graphene.ObjectType):
    reports = graphene.List(graphene.String)
    audit_log = graphene.List(graphene.String)
    system_config = graphene.String()

    @permission_required("reports.view_report")
    def resolve_reports(self, info):
        return ["q1", "q2"]

    @staff_member_required
    def resolve_audit_log(self, info):
        return ["login", "logout"]

    @superuser_required
    def resolve_system_config(self, info):
        return "{}"


schema = graphene.Schema(query=Query)

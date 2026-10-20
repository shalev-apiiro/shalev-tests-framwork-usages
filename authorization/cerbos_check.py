# Python.Cerbos.json -> "Cerbos Python" [Authorization]
# Expected: methods cerbos is_allowed, check_resources, plan_resources
from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, Resource, ResourceDesc, ResourceList

client = CerbosClient("http://localhost:3592")


def can_view(user_id: str, roles: list[str], document_id: str) -> bool:
    principal = Principal(user_id, roles=set(roles))
    resource = Resource(document_id, "document", attr={"owner": user_id})
    return client.is_allowed("view", principal, resource)


def check_many(user_id: str, roles: list[str], document_ids: list[str]):
    principal = Principal(user_id, roles=set(roles))
    resources = ResourceList()
    for document_id in document_ids:
        resources.add(Resource(document_id, "document"), {"view", "edit"})
    return client.check_resources(principal, resources)


def plan_viewable(user_id: str, roles: list[str]):
    principal = Principal(user_id, roles=set(roles))
    return client.plan_resources("view", principal, ResourceDesc("document"))

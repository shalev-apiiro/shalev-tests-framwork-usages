# Python.Cerbos.json -> "Cerbos Python" [Authorization]
# Expected: methods cerbos is_allowed, check_resources, plan_resources
import os

from cerbos.sdk.client import CerbosClient
from cerbos.sdk.model import Principal, PlanResourcesFilterKind, Resource, ResourceDesc, ResourceList

cerbos = CerbosClient(os.environ.get("CERBOS_URL", "http://cerbos:3592"), timeout_secs=1.5)


class Forbidden(Exception):
    pass


def _principal(user) -> Principal:
    return Principal(
        str(user.id),
        roles=set(user.roles),
        attr={"department": user.department, "region": user.region},
    )


def _resource(expense) -> Resource:
    return Resource(
        str(expense.id),
        "expense",
        attr={"owner": str(expense.owner_id), "amount": expense.amount, "region": expense.region},
    )


def require(user, action: str, expense) -> None:
    if not cerbos.is_allowed(action, _principal(user), _resource(expense)):
        raise Forbidden(f"{action} on expense {expense.id} denied")


def actions_per_expense(user, expenses) -> dict[str, set[str]]:
    resources = ResourceList()
    for expense in expenses:
        resources.add(_resource(expense), {"view", "approve", "delete"})
    response = cerbos.check_resources(_principal(user), resources)
    response.raise_if_failed()

    allowed = {}
    for expense in expenses:
        result = response.get_resource(str(expense.id))
        allowed[str(expense.id)] = {a for a in ("view", "approve", "delete") if result.is_allowed(a)}
    return allowed


def approvable_expenses_filter(user):
    plan = cerbos.plan_resources("approve", _principal(user), ResourceDesc("expense"))
    plan.raise_if_failed()
    if plan.filter.kind == PlanResourcesFilterKind.ALWAYS_ALLOWED:
        return {}
    if plan.filter.kind == PlanResourcesFilterKind.ALWAYS_DENIED:
        return None
    return plan.filter.condition.to_dict()

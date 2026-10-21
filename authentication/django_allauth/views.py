# Python.DjangoAllauth.json -> "Django Allauth Python" [Authentication]
# Expected: import allauth.account; decorators verified_email_required + reauthentication_required
from allauth.account.decorators import reauthentication_required, verified_email_required
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


@verified_email_required
def billing(request):
    invoices = request.user.invoices.order_by("-issued_at")[:24]
    return render(request, "billing/overview.html", {"invoices": invoices})


@verified_email_required
@require_http_methods(["GET", "POST"])
def invite_member(request):
    if request.method == "POST":
        request.user.organization.invitations.create(email=request.POST["email"], invited_by=request.user)
        messages.success(request, "Invitation sent.")
        return redirect("team")
    return render(request, "team/invite.html")


@reauthentication_required
@require_http_methods(["GET", "POST"])
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect("home")
    return render(request, "account/delete_confirm.html")

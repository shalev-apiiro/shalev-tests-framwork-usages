# Python.DjangoSessions.json -> "Django Sessions Python" [SessionManagement]
# Expected: import django.contrib.sessions; methods cycle_key, acycle_key
# (the methods are gated on the django.contrib.auth import)
from datetime import timedelta

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sessions.models import Session
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST


def end_other_sessions(user, keep_session_key: str) -> int:
    ended = 0
    for stored in Session.objects.filter(expire_date__gte=timezone.now()).exclude(session_key=keep_session_key):
        if stored.get_decoded().get("_auth_user_id") == str(user.pk):
            stored.delete()
            ended += 1
    return ended


@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        request.session.cycle_key()
        end_other_sessions(user, request.session.session_key)
        return redirect("account-settings")
    return render(request, "accounts/change_password.html", {"form": form})


@require_POST
@login_required
def enter_sudo_mode(request):
    if not request.user.check_password(request.POST.get("password", "")):
        return HttpResponseForbidden("wrong password")
    request.session.cycle_key()
    request.session["sudo_until"] = (timezone.now() + timedelta(minutes=10)).isoformat()
    return redirect(request.POST.get("next", "account-settings"))


async def refresh_session(request):
    user = await request.auser()
    if not user.is_authenticated:
        return JsonResponse({"error": "unauthenticated"}, status=401)
    await request.session.acycle_key()
    return JsonResponse({"rotated": True})

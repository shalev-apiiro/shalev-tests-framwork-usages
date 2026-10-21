# Python.DjangoOtp.json -> "Django OTP Python" [MultiFactorAuthentication]
# Expected: import django_otp; methods verify_token, match_token, random_token; decorator otp_required
import django_otp
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django_otp import devices_for_user, match_token, verify_token
from django_otp.decorators import otp_required
from django_otp.plugins.otp_static.models import StaticDevice, StaticToken

BACKUP_CODE_COUNT = 10


@login_required
@require_http_methods(["GET", "POST"])
def second_factor(request):
    devices = list(devices_for_user(request.user))
    if request.method == "GET":
        return render(request, "mfa/verify.html", {"devices": devices})

    token = request.POST["token"].strip()
    device_id = request.POST.get("device")
    device = verify_token(request.user, device_id, token) if device_id else match_token(request.user, token)
    if device is None:
        return render(request, "mfa/verify.html", {"devices": devices, "error": "Invalid code"}, status=401)

    django_otp.login(request, device)
    return redirect(request.GET.get("next", "dashboard"))


@otp_required
@require_http_methods(["POST"])
def regenerate_backup_codes(request):
    device, _ = StaticDevice.objects.get_or_create(user=request.user, name="backup")
    device.token_set.all().delete()
    codes = [StaticToken.random_token() for _ in range(BACKUP_CODE_COUNT)]
    StaticToken.objects.bulk_create(StaticToken(device=device, token=code) for code in codes)
    return render(request, "mfa/backup_codes.html", {"codes": codes})


@otp_required
def security_settings(request):
    return render(request, "mfa/settings.html", {"devices": list(devices_for_user(request.user))})

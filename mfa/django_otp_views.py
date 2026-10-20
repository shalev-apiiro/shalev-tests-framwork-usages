# Python.DjangoOtp.json -> "Django OTP Python" [MultiFactorAuthentication]
# Expected: import django_otp; methods verify_token, match_token, random_token; decorator otp_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django_otp import devices_for_user, match_token, verify_token
from django_otp.decorators import otp_required
from django_otp.plugins.otp_static.models import StaticDevice, StaticToken


@otp_required
def vault(request):
    return HttpResponse("second factor verified")


@login_required
def verify_second_factor(request):
    device = match_token(request.user, request.POST["token"])
    if device is None:
        return HttpResponse("invalid token", status=401)
    return HttpResponse("ok")


@login_required
def verify_named_device(request):
    device_id = request.POST["device"]
    device = verify_token(request.user, device_id, request.POST["token"])
    return HttpResponse("ok" if device else "invalid", status=200 if device else 401)


@login_required
def issue_backup_codes(request):
    device = StaticDevice.objects.get_or_create(user=request.user, name="backup")[0]
    codes = [StaticToken.random_token() for _ in range(10)]
    for code in codes:
        device.token_set.create(token=code)
    return HttpResponse("\n".join(codes))


def list_devices(user):
    return list(devices_for_user(user))

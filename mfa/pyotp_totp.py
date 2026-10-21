# Python.Pyotp.json -> "PyOTP Python" [MultiFactorAuthentication]
# Expected: import pyotp; methods TOTP, HOTP, random_base32, provisioning_uri
# Authenticator-app TOTP plus counter-based (HOTP) codes sent by email when the app is unavailable.
import pyotp

ISSUER = "Acme Cloud"


def start_enrollment(user) -> str:
    user.totp_secret = pyotp.random_base32()
    user.save(update_fields=["totp_secret"])
    return pyotp.TOTP(user.totp_secret).provisioning_uri(name=user.email, issuer_name=ISSUER)


def verify_app_code(user, code: str) -> bool:
    return pyotp.TOTP(user.totp_secret).verify(code, valid_window=1)


def send_email_code(user, mailer) -> None:
    if not user.email_otp_secret:
        user.email_otp_secret = pyotp.random_base32()
    user.email_otp_counter += 1
    user.save(update_fields=["email_otp_secret", "email_otp_counter"])
    code = pyotp.HOTP(user.email_otp_secret).at(user.email_otp_counter)
    mailer.send(user.email, "Your sign-in code", f"Your Acme Cloud sign-in code is {code}")


def verify_email_code(user, code: str) -> bool:
    if not pyotp.HOTP(user.email_otp_secret).verify(code, user.email_otp_counter):
        return False
    user.email_otp_counter += 1
    user.save(update_fields=["email_otp_counter"])
    return True

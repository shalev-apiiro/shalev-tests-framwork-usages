# Python.PythonJose.json -> "Python Jose Python" [Authentication]
# Expected: methods jose.jwt.decode + jose.jws.verify
from jose import JWTError, jws, jwt

SECRET = "change-me"


def issue_token(subject: str) -> str:
    return jwt.encode({"sub": subject}, SECRET, algorithm="HS256")


def authenticate(token: str) -> str | None:
    try:
        claims = jwt.decode(token, SECRET, algorithms=["HS256"])
    except JWTError:
        return None
    return claims.get("sub")


def verify_signature(token: str) -> bytes:
    return jws.verify(token, SECRET, algorithms=["HS256"])

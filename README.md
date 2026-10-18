# shalev-tests-framwork-usages

Samples for apiiro/lim PR #53550 (Python SessionManagement framework usages). One file per new config.

| File | Config | Expected framework | Should match |
| --- | --- | --- | --- |
| `aiohttp_session_app.py` | `Python.AiohttpSession.json` | aiohttp-session Python | import `aiohttp_session`, `new_session`, `invalidate` |
| `django_sessions_views.py` | `Python.DjangoSessions.json` | Django Sessions Python | import `django.contrib.sessions...`, `cycle_key`, `acycle_key`, `logout`, `alogout` |
| `flask_builtin_session_app.py` | `Python.FlaskBuiltInSession.json` | Flask Session Python | `from flask import session` |
| `flask_session_app.py` | `Python.FlaskSession.json` | Flask-Session Python | import `flask_session`, `regenerate` |
| `flask_login_logout.py` | `Python.FlaskLoginSession.json` | Flask-Login Session Python | `logout_user` |
| `starlette_sessions_app.py` | `Python.StarletteSessionMiddleware.json` | Starlette Sessions Python | import `starlette.middleware.sessions` |

import json
from datetime import date
from functools import wraps

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core import signing
from django.http import HttpRequest
from django.shortcuts import redirect

from ..permissions import can_manage_dashboard_data, can_manage_users

RECENT_PROFILES_COOKIE = "tourismo_recent_profiles"
RECENT_PROFILES_LIMIT = 5
RECENT_PROFILES_MAX_AGE = 60 * 60 * 24 * 30
RECENT_PROFILE_TOKEN_SALT = "agency.saved-profile-login"


def _first_day_of_month(value: date) -> date:
    return value.replace(day=1)


def _shift_month(value: date, months_back: int) -> date:
    year = value.year
    month = value.month - months_back
    while month <= 0:
        year -= 1
        month += 12
    return date(year, month, 1)


def _to_bool(post_data, key: str) -> bool:
    return bool(post_data.get(key))


def _load_recent_profiles(request: HttpRequest):
    raw_profiles = request.COOKIES.get(RECENT_PROFILES_COOKIE, "[]")
    try:
        parsed = json.loads(raw_profiles)
    except json.JSONDecodeError:
        return []

    profiles = []
    for profile in parsed:
        if not isinstance(profile, dict):
            continue
        username = str(profile.get("username", "")).strip()
        display_name = str(profile.get("display_name", "")).strip()
        if not username:
            continue
        profiles.append(
            {
                "username": username,
                "display_name": display_name or username,
                "token": str(profile.get("token", "")).strip(),
            }
        )
    return profiles[:RECENT_PROFILES_LIMIT]


def _build_recent_profile(user):
    return {
        "username": user.username,
        "display_name": user.get_full_name() or user.username,
        "token": signing.dumps(
            {"uid": user.pk, "pwd": user.password}, salt=RECENT_PROFILE_TOKEN_SALT
        ),
    }


def _set_recent_profiles_cookie(response, profiles):
    response.set_cookie(
        RECENT_PROFILES_COOKIE,
        json.dumps(profiles[:RECENT_PROFILES_LIMIT]),
        max_age=RECENT_PROFILES_MAX_AGE,
        samesite="Lax",
    )


def _clear_recent_profiles_cookie(response):
    response.delete_cookie(RECENT_PROFILES_COOKIE, samesite="Lax")


def _create_notification(request, title: str, message: str, link: str = ""):
    if not request.user.is_authenticated:
        return

    User = get_user_model()
    actor = request.user
    actor_details = actor.get_full_name().strip() or actor.username
    actor_signature = f"{actor_details} (@{actor.username})"
    recipients = User.objects.filter(is_active=True).only("id")
    NotificationModel = actor.notifications.model
    NotificationModel.objects.bulk_create(
        [
            NotificationModel(
                user=user,
                title=title,
                message=(
                    message
                    if user.pk == actor.pk
                    else f"{message} Updated by {actor_signature}."
                ),
                link=link,
            )
            for user in recipients
        ]
    )


def _forbidden_redirect(request: HttpRequest, message: str):
    messages.error(request, message)
    return redirect("dashboard")


def require_data_management(view_func):
    @wraps(view_func)
    def _wrapped(request: HttpRequest, *args, **kwargs):
        if not can_manage_dashboard_data(request.user):
            return _forbidden_redirect(
                request, "You can view data but only managers/superusers can modify it."
            )
        return view_func(request, *args, **kwargs)

    return _wrapped


def require_user_management(view_func):
    @wraps(view_func)
    def _wrapped(request: HttpRequest, *args, **kwargs):
        if not can_manage_users(request.user):
            return _forbidden_redirect(
                request, "You can only view your own profile with your current role."
            )
        return view_func(request, *args, **kwargs)

    return _wrapped

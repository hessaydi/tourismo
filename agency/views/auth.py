from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from ..permissions import NORMAL_ROLE, assign_role
from .shared import (
    RECENT_PROFILES_MAX_AGE,
    RECENT_PROFILE_TOKEN_SALT,
    _build_recent_profile,
    _clear_recent_profiles_cookie,
    _load_recent_profiles,
    _set_recent_profiles_cookie,
)


class AccountLoginView(LoginView):
    template_name = "registration/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_profiles"] = _load_recent_profiles(self.request)
        context["prefill_username"] = self.request.GET.get("username", "").strip()
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        current_profile = _build_recent_profile(form.get_user())
        existing = [
            p
            for p in _load_recent_profiles(self.request)
            if p.get("username") != current_profile["username"]
        ]
        _set_recent_profiles_cookie(response, [current_profile, *existing])
        return response


class AccountLogoutView(LogoutView):
    template_name = "registration/logged_out.html"
    next_page = "logout"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_profiles"] = _load_recent_profiles(self.request)
        return context


@require_POST
def saved_profile_login(request):
    token = request.POST.get("token", "").strip()
    if not token:
        messages.error(request, "Saved profile token is missing.")
        return redirect("login")

    try:
        payload = signing.loads(
            token, salt=RECENT_PROFILE_TOKEN_SALT, max_age=RECENT_PROFILES_MAX_AGE
        )
    except (BadSignature, SignatureExpired):
        messages.error(request, "Saved profile expired. Please login with password.")
        return redirect("login")

    User = get_user_model()
    user = User.objects.filter(pk=payload.get("uid"), is_active=True).first()
    if not user or payload.get("pwd") != user.password:
        messages.error(request, "Saved profile is no longer valid.")
        return redirect("login")

    login(request, user)
    current_profile = _build_recent_profile(user)
    existing = [
        p
        for p in _load_recent_profiles(request)
        if p.get("username") != current_profile["username"]
    ]
    next_url = request.POST.get("next", "").strip()
    success_url = reverse("dashboard")
    if next_url and url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        success_url = next_url
    response = redirect(success_url)
    _set_recent_profiles_cookie(response, [current_profile, *existing])
    return response


@require_POST
def clear_saved_profiles(request):
    response = redirect("login")
    _clear_recent_profiles_cookie(response)
    messages.success(request, "Saved profiles cleared.")
    return response


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            assign_role(user, NORMAL_ROLE)
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})

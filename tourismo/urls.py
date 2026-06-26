from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from agency import views as agency_views


def health(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health),
    path("accounts/login/", agency_views.AccountLoginView.as_view(), name="login"),
    path("accounts/saved-login/", agency_views.saved_profile_login, name="saved_profile_login"),
    path(
        "accounts/saved-profiles/clear/",
        agency_views.clear_saved_profiles,
        name="clear_saved_profiles",
    ),
    path("accounts/register/", agency_views.register, name="register"),
    path("accounts/logout/", agency_views.AccountLogoutView.as_view(), name="logout"),
    path("", include("agency.urls")),
]

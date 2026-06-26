from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("", login_required(views.dashboard), name="dashboard"),
    path("users/", login_required(views.users_list), name="users_list"),
    path("users/new/", login_required(views.user_create), name="user_create"),
    path("users/<int:pk>/", login_required(views.user_profile), name="user_profile"),
    path("users/<int:pk>/edit/", login_required(views.user_edit), name="user_edit"),
    path("users/<int:pk>/delete/", login_required(views.user_delete), name="user_delete"),
    path(
        "admin-control/", views.admin_control_dashboard, name="admin_control_dashboard"
    ),
    path(
        "notifications/",
        login_required(views.notifications_list),
        name="notifications_list",
    ),
    path(
        "notifications/<int:pk>/read/",
        login_required(views.notification_mark_read),
        name="notification_mark_read",
    ),
    # Packages
    path("packages/", login_required(views.packages_list), name="packages_list"),
    path("packages/new/", login_required(views.package_create), name="package_create"),
    path("packages/<int:pk>/edit/", login_required(views.package_edit), name="package_edit"),
    path(
        "packages/<int:pk>/delete/",
        login_required(views.package_delete),
        name="package_delete",
    ),
    # Clients
    path("clients/", login_required(views.clients_list), name="clients_list"),
    path("clients/new/", login_required(views.client_create), name="client_create"),
    path("clients/<int:pk>/", login_required(views.client_detail), name="client_detail"),
    path("clients/<int:pk>/edit/", login_required(views.client_edit), name="client_edit"),
    path("clients/<int:pk>/delete/", login_required(views.client_delete), name="client_delete"),
    # Bookings
    path("bookings/", login_required(views.bookings_list), name="bookings_list"),
    path("bookings/new/", login_required(views.booking_create), name="booking_create"),
    path("bookings/<int:pk>/edit/", login_required(views.booking_edit), name="booking_edit"),
    path(
        "bookings/<int:pk>/delete/",
        login_required(views.booking_delete),
        name="booking_delete",
    ),
    # Destinations
    path(
        "destinations/",
        login_required(views.destinations_list),
        name="destinations_list",
    ),
    path(
        "destinations/new/",
        login_required(views.destination_create),
        name="destination_create",
    ),
    path(
        "destinations/<int:pk>/edit/",
        login_required(views.destination_edit),
        name="destination_edit",
    ),
    path(
        "destinations/<int:pk>/delete/",
        login_required(views.destination_delete),
        name="destination_delete",
    ),
    # Guides
    path("guides/", login_required(views.guides_list), name="guides_list"),
    path("guides/new/", login_required(views.guide_create), name="guide_create"),
    path("guides/<int:pk>/edit/", login_required(views.guide_edit), name="guide_edit"),
    path("guides/<int:pk>/delete/", login_required(views.guide_delete), name="guide_delete"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path(
        "admin-control/", views.admin_control_dashboard, name="admin_control_dashboard"
    ),
    # Packages
    path("packages/", views.packages_list, name="packages_list"),
    path("packages/new/", views.package_create, name="package_create"),
    path("packages/<int:pk>/edit/", views.package_edit, name="package_edit"),
    path("packages/<int:pk>/delete/", views.package_delete, name="package_delete"),
    # Clients
    path("clients/", views.clients_list, name="clients_list"),
    path("clients/new/", views.client_create, name="client_create"),
    path("clients/<int:pk>/", views.client_detail, name="client_detail"),
    path("clients/<int:pk>/edit/", views.client_edit, name="client_edit"),
    path("clients/<int:pk>/delete/", views.client_delete, name="client_delete"),
    # Bookings
    path("bookings/", views.bookings_list, name="bookings_list"),
    path("bookings/new/", views.booking_create, name="booking_create"),
    path("bookings/<int:pk>/edit/", views.booking_edit, name="booking_edit"),
    path("bookings/<int:pk>/delete/", views.booking_delete, name="booking_delete"),
    # Destinations
    path("destinations/", views.destinations_list, name="destinations_list"),
    path("destinations/new/", views.destination_create, name="destination_create"),
    path(
        "destinations/<int:pk>/edit/", views.destination_edit, name="destination_edit"
    ),
    path(
        "destinations/<int:pk>/delete/",
        views.destination_delete,
        name="destination_delete",
    ),
    # Guides
    path("guides/", views.guides_list, name="guides_list"),
    path("guides/new/", views.guide_create, name="guide_create"),
    path("guides/<int:pk>/edit/", views.guide_edit, name="guide_edit"),
    path("guides/<int:pk>/delete/", views.guide_delete, name="guide_delete"),
]

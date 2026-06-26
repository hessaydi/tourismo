from django.contrib import admin

from .models import Destination, Package, Client, Booking, Guide, Notification


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "is_featured", "created_at")
    list_filter = ("is_featured", "country")
    search_fields = ("name", "country")


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "destination",
        "category",
        "status",
        "price_per_person",
        "max_capacity",
    )
    list_filter = ("status", "category", "destination")
    search_fields = ("title", "destination__name")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "nationality",
        "created_at",
    )
    search_fields = ("first_name", "last_name", "email", "passport_number")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "booking_ref",
        "client",
        "package",
        "travel_date",
        "status",
        "payment_status",
        "total_price",
    )
    list_filter = ("status", "payment_status", "travel_date")
    search_fields = (
        "booking_ref",
        "client__first_name",
        "client__last_name",
        "package__title",
    )


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "languages", "rating", "is_available")
    list_filter = ("is_available",)
    search_fields = ("name", "email", "languages", "specialties")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("title", "message", "user__username")

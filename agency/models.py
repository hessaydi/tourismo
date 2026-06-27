from django.db import models
from django.contrib.auth import get_user_model

from .constants import (
    BOOKING_PAYMENT_STATUS_CHOICES,
    BOOKING_REF_DIGITS,
    BOOKING_REF_PREFIX,
    BOOKING_STATUS_CHOICES,
    PACKAGE_CATEGORY_CHOICES,
    PACKAGE_STATUS_CHOICES,
)


class Destination(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.country}"


class Package(models.Model):
    CATEGORY_CHOICES = PACKAGE_CATEGORY_CHOICES
    STATUS_CHOICES = PACKAGE_STATUS_CHOICES
    title = models.CharField(max_length=200)
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name="packages"
    )
    bookings_rows = models.ManyToManyField("Booking", blank=True, related_name="packages")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    duration_days = models.PositiveIntegerField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    max_capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    includes = models.TextField(
        blank=True, help_text="What is included (comma-separated)"
    )
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title}"

    @property
    def bookings(self) -> int:
        return Booking.objects.filter(
            packages=self, status__in=["confirmed", "pending"]
        ).count()


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30)
    passport_number = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self) -> str:
        """
        The `full_name` function in Python returns the full name by concatenating the `first_name` and
        `last_name` attributes of an object.
        :return: The `full_name` method is returning a string that concatenates the `first_name` and
        `last_name` attributes of the object with a space in between.
        """
        return f"{self.first_name} {self.last_name}"

    @property
    def total_bookings(self) -> int:
        """
        The `total_bookings` function in Python returns the total number of bookings associated with a client.
        :return: The `total_bookings` method is returning an integer representing the count of bookings.
        """
        return self.bookings.count()


# This class represents a booking model in a Python application.
class Booking(models.Model):
    STATUS_CHOICES = BOOKING_STATUS_CHOICES
    PAYMENT_STATUS = BOOKING_PAYMENT_STATUS_CHOICES
    booking_ref = models.CharField(max_length=20, unique=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="bookings"
    )
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="bookings"
    )
    travel_date = models.DateField()
    return_date = models.DateField()
    num_travelers = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS, default="unpaid"
    )
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking_ref} - {self.client.full_name}"

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            import random
            import string

            self.booking_ref = BOOKING_REF_PREFIX + "".join(
                random.choices(string.digits, k=BOOKING_REF_DIGITS)
            )
        if not self.total_price:
            self.total_price = self.package.price_per_person * self.num_travelers
        super().save(*args, **kwargs)


# The above class is a model named Guide in a Python application.
class Guide(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30)
    languages = models.CharField(max_length=200, help_text="Comma-separated languages")
    specialties = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Notification(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=180)
    message = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.user})"

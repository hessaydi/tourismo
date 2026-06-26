import json
from datetime import date

from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from ..models import Booking, Client, Destination, Guide, Notification, Package
from .shared import (
    _create_notification,
    _first_day_of_month,
    _shift_month,
    _to_bool,
    require_data_management,
)


@require_data_management
def admin_control_dashboard(request):
    today = date.today()
    paid_revenue = (
        Booking.objects.filter(payment_status="paid").aggregate(Sum("total_price"))[
            "total_price__sum"
        ]
        or 0
    )

    context = {
        "active_packages": Package.objects.filter(status="active").count(),
        "inactive_packages": Package.objects.filter(status="inactive").count(),
        "featured_destinations": Destination.objects.filter(is_featured=True).count(),
        "unavailable_guides": Guide.objects.filter(is_available=False).count(),
        "pending_bookings": Booking.objects.filter(status="pending").count(),
        "unpaid_bookings": Booking.objects.filter(payment_status="unpaid").count(),
        "upcoming_confirmed": Booking.objects.filter(
            travel_date__gte=today, status="confirmed"
        ).count(),
        "paid_revenue": paid_revenue,
        "recent_bookings": Booking.objects.select_related("client", "package").order_by(
            "-created_at"
        )[:6],
        "recent_clients": Client.objects.order_by("-created_at")[:6],
    }
    return render(request, "agency/admin_control_dashboard.html", context)


def dashboard(request):
    today = date.today()
    total_bookings = Booking.objects.count()
    confirmed = Booking.objects.filter(status="confirmed").count()
    revenue = (
        Booking.objects.filter(payment_status="paid").aggregate(Sum("total_price"))[
            "total_price__sum"
        ]
        or 0
    )
    clients = Client.objects.count()
    packages = Package.objects.filter(status="active").count()
    pending = Booking.objects.filter(status="pending").count()
    upcoming = Booking.objects.filter(travel_date__gte=today, status="confirmed").count()
    recent_bookings = Booking.objects.select_related("client", "package").order_by(
        "-created_at"
    )[:8]
    top_packages = Package.objects.annotate(b_count=Count("bookings")).order_by("-b_count")[
        :5
    ]

    monthly_data = []
    for i in range(5, -1, -1):
        month_start = _shift_month(_first_day_of_month(today), i)
        rev = (
            Booking.objects.filter(
                created_at__year=month_start.year,
                created_at__month=month_start.month,
                payment_status="paid",
            ).aggregate(Sum("total_price"))["total_price__sum"]
            or 0
        )
        monthly_data.append({"month": month_start.strftime("%b"), "revenue": float(rev)})

    context = {
        "total_bookings": total_bookings,
        "confirmed": confirmed,
        "revenue": revenue,
        "clients": clients,
        "packages": packages,
        "pending": pending,
        "upcoming": upcoming,
        "recent_bookings": recent_bookings,
        "top_packages": top_packages,
        "monthly_data": json.dumps(monthly_data),
    }
    return render(request, "agency/dashboard.html", context)


def packages_list(request):
    q = request.GET.get("q", "")
    cat = request.GET.get("category", "")
    packages = (
        Package.objects.select_related("destination")
        .annotate(b_count=Count("bookings"))
        .order_by("-created_at")
    )
    if q:
        packages = packages.filter(
            Q(title__icontains=q) | Q(destination__name__icontains=q)
        )
    if cat:
        packages = packages.filter(category=cat)
    return render(
        request,
        "agency/packages.html",
        {
            "packages": packages,
            "q": q,
            "cat": cat,
            "categories": Package.CATEGORY_CHOICES,
        },
    )


@require_data_management
def package_create(request):
    if request.method == "POST":
        package = Package(
            title=request.POST["title"],
            destination_id=request.POST["destination"],
            category=request.POST["category"],
            description=request.POST["description"],
            duration_days=request.POST["duration_days"],
            price_per_person=request.POST["price_per_person"],
            max_capacity=request.POST["max_capacity"],
            status=request.POST.get("status", "active"),
            includes=request.POST.get("includes", ""),
            image_url=request.POST.get("image_url", ""),
        )
        package.save()
        _create_notification(
            request,
            "Package created",
            f"{package.title} was added to catalog.",
            link="/packages/",
        )
        messages.success(request, "Package created successfully.")
        return redirect("packages_list")
    return render(
        request,
        "agency/package_form.html",
        {
            "destinations": Destination.objects.all(),
            "categories": Package.CATEGORY_CHOICES,
            "statuses": Package.STATUS_CHOICES,
        },
    )


@require_data_management
def package_edit(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == "POST":
        package.title = request.POST["title"]
        package.destination_id = request.POST["destination"]
        package.category = request.POST["category"]
        package.description = request.POST["description"]
        package.duration_days = request.POST["duration_days"]
        package.price_per_person = request.POST["price_per_person"]
        package.max_capacity = request.POST["max_capacity"]
        package.status = request.POST.get("status", "active")
        package.includes = request.POST.get("includes", "")
        package.image_url = request.POST.get("image_url", "")
        package.save()
        _create_notification(
            request,
            "Package updated",
            f"{package.title} details were updated.",
            link="/packages/",
        )
        messages.success(request, "Package updated successfully.")
        return redirect("packages_list")
    return render(
        request,
        "agency/package_form.html",
        {
            "package": package,
            "destinations": Destination.objects.all(),
            "categories": Package.CATEGORY_CHOICES,
            "statuses": Package.STATUS_CHOICES,
        },
    )


@require_data_management
def package_delete(request, pk):
    package = get_object_or_404(Package, pk=pk)
    package_title = package.title
    package.delete()
    _create_notification(
        request,
        "Package deleted",
        f"{package_title} was removed from catalog.",
        link="/packages/",
    )
    messages.success(request, "Package deleted successfully.")
    return redirect("packages_list")


def clients_list(request):
    q = request.GET.get("q", "")
    clients = Client.objects.annotate(b_count=Count("bookings")).order_by("-created_at")
    if q:
        clients = clients.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q)
        )
    return render(request, "agency/clients.html", {"clients": clients, "q": q})


@require_data_management
def client_create(request):
    if request.method == "POST":
        client = Client(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            passport_number=request.POST.get("passport_number", ""),
            nationality=request.POST.get("nationality", ""),
            address=request.POST.get("address", ""),
            notes=request.POST.get("notes", ""),
        )
        if request.POST.get("date_of_birth"):
            client.date_of_birth = request.POST["date_of_birth"]
        client.save()
        _create_notification(
            request,
            "Client added",
            f"{client.full_name} profile was created.",
            link="/clients/",
        )
        messages.success(request, "Client created successfully.")
        return redirect("clients_list")
    return render(request, "agency/client_form.html", {})


@require_data_management
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        client.first_name = request.POST["first_name"]
        client.last_name = request.POST["last_name"]
        client.email = request.POST["email"]
        client.phone = request.POST["phone"]
        client.passport_number = request.POST.get("passport_number", "")
        client.nationality = request.POST.get("nationality", "")
        client.address = request.POST.get("address", "")
        client.notes = request.POST.get("notes", "")
        if request.POST.get("date_of_birth"):
            client.date_of_birth = request.POST["date_of_birth"]
        client.save()
        _create_notification(
            request,
            "Client updated",
            f"{client.full_name} profile was updated.",
            link="/clients/",
        )
        messages.success(request, "Client updated successfully.")
        return redirect("clients_list")
    return render(request, "agency/client_form.html", {"client": client})


@require_data_management
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client_name = client.full_name
    client.delete()
    _create_notification(
        request, "Client deleted", f"{client_name} was deleted.", link="/clients/"
    )
    messages.success(request, "Client deleted successfully.")
    return redirect("clients_list")


def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    bookings = client.bookings.select_related("package").order_by("-created_at")
    return render(request, "agency/client_detail.html", {"client": client, "bookings": bookings})


def bookings_list(request):
    q = request.GET.get("q", "")
    status = request.GET.get("status", "")
    bookings = Booking.objects.select_related("client", "package").order_by("-created_at")
    if q:
        bookings = bookings.filter(
            Q(booking_ref__icontains=q)
            | Q(client__first_name__icontains=q)
            | Q(client__last_name__icontains=q)
        )
    if status:
        bookings = bookings.filter(status=status)
    return render(
        request,
        "agency/bookings.html",
        {
            "bookings": bookings,
            "q": q,
            "status": status,
            "statuses": Booking.STATUS_CHOICES,
        },
    )


@require_data_management
def booking_create(request):
    if request.method == "POST":
        package = get_object_or_404(Package, pk=request.POST["package"])
        num_travelers = int(request.POST.get("num_travelers", 1))
        booking = Booking(
            client_id=request.POST["client"],
            package=package,
            travel_date=request.POST["travel_date"],
            return_date=request.POST["return_date"],
            num_travelers=num_travelers,
            total_price=package.price_per_person * num_travelers,
            status=request.POST.get("status", "pending"),
            payment_status=request.POST.get("payment_status", "unpaid"),
            special_requests=request.POST.get("special_requests", ""),
        )
        booking.save()
        _create_notification(
            request,
            "Booking created",
            f"{booking.booking_ref} was created for {booking.client.full_name}.",
            link="/bookings/",
        )
        messages.success(request, "Booking created successfully.")
        return redirect("bookings_list")
    return render(
        request,
        "agency/booking_form.html",
        {
            "clients": Client.objects.all(),
            "packages": Package.objects.filter(status="active"),
            "statuses": Booking.STATUS_CHOICES,
            "payment_statuses": Booking.PAYMENT_STATUS,
        },
    )


@require_data_management
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == "POST":
        booking.client_id = request.POST["client"]
        booking.package_id = request.POST["package"]
        booking.travel_date = request.POST["travel_date"]
        booking.return_date = request.POST["return_date"]
        booking.num_travelers = int(request.POST.get("num_travelers", 1))
        booking.total_price = request.POST["total_price"]
        booking.status = request.POST.get("status", "pending")
        booking.payment_status = request.POST.get("payment_status", "unpaid")
        booking.special_requests = request.POST.get("special_requests", "")
        booking.save()
        _create_notification(
            request,
            "Booking updated",
            f"{booking.booking_ref} was updated.",
            link="/bookings/",
        )
        messages.success(request, "Booking updated successfully.")
        return redirect("bookings_list")
    return render(
        request,
        "agency/booking_form.html",
        {
            "booking": booking,
            "clients": Client.objects.all(),
            "packages": Package.objects.filter(status="active"),
            "statuses": Booking.STATUS_CHOICES,
            "payment_statuses": Booking.PAYMENT_STATUS,
        },
    )


@require_data_management
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking_ref = booking.booking_ref
    booking.delete()
    _create_notification(request, "Booking deleted", f"{booking_ref} was deleted.", link="/bookings/")
    messages.success(request, "Booking deleted successfully.")
    return redirect("bookings_list")


def destinations_list(request):
    destinations = Destination.objects.annotate(pkg_count=Count("packages")).order_by(
        "-created_at"
    )
    return render(request, "agency/destinations.html", {"destinations": destinations})


@require_data_management
def destination_create(request):
    if request.method == "POST":
        destination = Destination(
            name=request.POST["name"],
            country=request.POST["country"],
            description=request.POST["description"],
            image_url=request.POST.get("image_url", ""),
            is_featured=_to_bool(request.POST, "is_featured"),
        )
        destination.save()
        _create_notification(
            request,
            "Destination created",
            f"{destination.name}, {destination.country} was added.",
            link="/destinations/",
        )
        messages.success(request, "Destination created successfully.")
        return redirect("destinations_list")
    return render(request, "agency/destination_form.html", {})


@require_data_management
def destination_edit(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == "POST":
        destination.name = request.POST["name"]
        destination.country = request.POST["country"]
        destination.description = request.POST["description"]
        destination.image_url = request.POST.get("image_url", "")
        destination.is_featured = _to_bool(request.POST, "is_featured")
        destination.save()
        _create_notification(
            request,
            "Destination updated",
            f"{destination.name}, {destination.country} was updated.",
            link="/destinations/",
        )
        messages.success(request, "Destination updated successfully.")
        return redirect("destinations_list")
    return render(request, "agency/destination_form.html", {"destination": destination})


@require_data_management
def destination_delete(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    destination_name = str(destination)
    destination.delete()
    _create_notification(
        request,
        "Destination deleted",
        f"{destination_name} was removed.",
        link="/destinations/",
    )
    messages.success(request, "Destination deleted successfully.")
    return redirect("destinations_list")


def guides_list(request):
    guides = Guide.objects.all().order_by("-created_at")
    return render(request, "agency/guides.html", {"guides": guides})


@require_data_management
def guide_create(request):
    if request.method == "POST":
        guide = Guide(
            name=request.POST["name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            languages=request.POST["languages"],
            specialties=request.POST.get("specialties", ""),
            bio=request.POST.get("bio", ""),
            rating=request.POST.get("rating", 5.0),
            is_available=_to_bool(request.POST, "is_available"),
        )
        guide.save()
        _create_notification(
            request,
            "Guide created",
            f"{guide.name} profile was created.",
            link="/guides/",
        )
        messages.success(request, "Guide created successfully.")
        return redirect("guides_list")
    return render(request, "agency/guide_form.html", {})


@require_data_management
def guide_edit(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    if request.method == "POST":
        guide.name = request.POST["name"]
        guide.email = request.POST["email"]
        guide.phone = request.POST["phone"]
        guide.languages = request.POST["languages"]
        guide.specialties = request.POST.get("specialties", "")
        guide.bio = request.POST.get("bio", "")
        guide.rating = request.POST.get("rating", 5.0)
        guide.is_available = _to_bool(request.POST, "is_available")
        guide.save()
        _create_notification(
            request,
            "Guide updated",
            f"{guide.name} profile was updated.",
            link="/guides/",
        )
        messages.success(request, "Guide updated successfully.")
        return redirect("guides_list")
    return render(request, "agency/guide_form.html", {"guide": guide})


@require_data_management
def guide_delete(request, pk):
    guide = get_object_or_404(Guide, pk=pk)
    guide_name = guide.name
    guide.delete()
    _create_notification(request, "Guide deleted", f"{guide_name} was removed.", link="/guides/")
    messages.success(request, "Guide deleted successfully.")
    return redirect("guides_list")


def notifications_list(request):
    notifications = request.user.notifications.all()
    return render(request, "agency/notifications.html", {"notifications": notifications})


def notification_mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])

    next_url = request.GET.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("notifications_list")

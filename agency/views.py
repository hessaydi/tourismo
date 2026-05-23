import json
from datetime import date

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q
from django.shortcuts import render, get_object_or_404, redirect

from .models import Destination, Package, Client, Booking, Guide


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


@staff_member_required
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
    upcoming = Booking.objects.filter(
        travel_date__gte=today, status="confirmed"
    ).count()
    recent_bookings = Booking.objects.select_related("client", "package").order_by(
        "-created_at"
    )[:8]
    top_packages = Package.objects.annotate(b_count=Count("bookings")).order_by(
        "-b_count"
    )[:5]

    # Monthly revenue for chart (last 6 complete/current months)
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
        monthly_data.append(
            {"month": month_start.strftime("%b"), "revenue": float(rev)}
        )

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


# ── PACKAGES ─────────────────────────────────────────────────────────────────
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


def package_delete(_request, pk):
    get_object_or_404(Package, pk=pk).delete()
    return redirect("packages_list")


# ── CLIENTS ───────────────────────────────────────────────────────────────────
def clients_list(request):
    q = request.GET.get("q", "")
    clients = Client.objects.annotate(b_count=Count("bookings")).order_by("-created_at")
    if q:
        clients = clients.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(email__icontains=q)
        )
    return render(request, "agency/clients.html", {"clients": clients, "q": q})


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
        return redirect("clients_list")
    return render(request, "agency/client_form.html", {})


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
        return redirect("clients_list")
    return render(request, "agency/client_form.html", {"client": client})


def client_delete(_request, pk):
    get_object_or_404(Client, pk=pk).delete()
    return redirect("clients_list")


def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    bookings = client.bookings.select_related("package").order_by("-created_at")
    return render(
        request, "agency/client_detail.html", {"client": client, "bookings": bookings}
    )


# ── BOOKINGS ──────────────────────────────────────────────────────────────────
def bookings_list(request):
    q = request.GET.get("q", "")
    status = request.GET.get("status", "")
    bookings = Booking.objects.select_related("client", "package").order_by(
        "-created_at"
    )
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


def booking_delete(_request, pk):
    get_object_or_404(Booking, pk=pk).delete()
    return redirect("bookings_list")


# ── DESTINATIONS ─────────────────────────────────────────────────────────────
def destinations_list(request):
    destinations = Destination.objects.annotate(pkg_count=Count("packages")).order_by(
        "-created_at"
    )
    return render(request, "agency/destinations.html", {"destinations": destinations})


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
        return redirect("destinations_list")
    return render(request, "agency/destination_form.html", {})


def destination_edit(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == "POST":
        destination.name = request.POST["name"]
        destination.country = request.POST["country"]
        destination.description = request.POST["description"]
        destination.image_url = request.POST.get("image_url", "")
        destination.is_featured = _to_bool(request.POST, "is_featured")
        destination.save()
        return redirect("destinations_list")
    return render(request, "agency/destination_form.html", {"destination": destination})


def destination_delete(_request, pk):
    get_object_or_404(Destination, pk=pk).delete()
    return redirect("destinations_list")


# ── GUIDES ────────────────────────────────────────────────────────────────────
def guides_list(request):
    guides = Guide.objects.all().order_by("-created_at")
    return render(request, "agency/guides.html", {"guides": guides})


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
        return redirect("guides_list")
    return render(request, "agency/guide_form.html", {})


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
        return redirect("guides_list")
    return render(request, "agency/guide_form.html", {"guide": guide})


def guide_delete(_request, pk):
    get_object_or_404(Guide, pk=pk).delete()
    return redirect("guides_list")

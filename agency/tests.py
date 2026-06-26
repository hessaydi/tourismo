from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Booking, Client, Destination, Guide, Notification, Package
from .permissions import MANAGER_GROUP_NAME, assign_role
from .views import RECENT_PROFILES_COOKIE


class AuthenticationAccessTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="agent1", password="secure-pass-123"
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_dashboard_accessible_when_logged_in(self):
        self.client.login(username="agent1", password="secure-pass-123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_register_page_accessible_when_logged_out(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "agent3",
                "password1": "strong-pass-1234",
                "password2": "strong-pass-1234",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(get_user_model().objects.filter(username="agent3").exists())
        self.assertIn("_auth_user_id", self.client.session)

    def test_register_redirects_authenticated_user(self):
        self.client.login(username="agent1", password="secure-pass-123")
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"))

    def test_logout_page_shows_saved_login_profile(self):
        self.client.post(
            reverse("login"),
            {"username": "agent1", "password": "secure-pass-123"},
        )
        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Choose a saved profile")
        self.assertContains(response, "@agent1")

    def test_login_page_prefills_username_from_saved_profile(self):
        self.client.post(
            reverse("login"),
            {"username": "agent1", "password": "secure-pass-123"},
        )
        self.client.post(reverse("logout"))
        response = self.client.get(reverse("login"), {"username": "agent1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="agent1"', html=False)

    def test_saved_profile_login_without_password(self):
        self.client.post(
            reverse("login"),
            {"username": "agent1", "password": "secure-pass-123"},
        )
        logout_response = self.client.post(reverse("logout"))
        profile = logout_response.context["recent_profiles"][0]
        response = self.client.post(
            reverse("saved_profile_login"),
            {"token": profile["token"]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"))
        self.assertEqual(str(self.client.session["_auth_user_id"]), str(self.user.pk))

    def test_clear_saved_profiles_button(self):
        self.client.post(
            reverse("login"),
            {"username": "agent1", "password": "secure-pass-123"},
        )
        self.client.post(reverse("logout"))
        response = self.client.post(reverse("clear_saved_profiles"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
        self.assertIn(RECENT_PROFILES_COOKIE, response.cookies)
        self.assertEqual(response.cookies[RECENT_PROFILES_COOKIE]["max-age"], 0)
        cookie_value = self.client.cookies.get(RECENT_PROFILES_COOKIE)
        if cookie_value:
            self.assertEqual(cookie_value.value, "")


class NotificationsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="agent2", password="secure-pass-123"
        )
        self.other_user = get_user_model().objects.create_user(
            username="agent3", password="secure-pass-123"
        )
        assign_role(self.user, "manager")
        assign_role(self.other_user, "normal")
        self.destination = Destination.objects.create(
            name="Marrakech",
            country="Morocco",
            description="City break package",
        )
        self.package = Package.objects.create(
            title="Marrakech Explorer",
            destination=self.destination,
            category="adventure",
            description="3 nights trip",
            duration_days=3,
            price_per_person=1000,
            max_capacity=20,
            status="active",
        )
        self.client_profile = Client.objects.create(
            first_name="Sara",
            last_name="Alaoui",
            email="sara@example.com",
            phone="+212600000000",
        )

    def test_booking_creation_generates_notification(self):
        self.client.login(username="agent2", password="secure-pass-123")
        response = self.client.post(
            reverse("booking_create"),
            {
                "client": self.client_profile.pk,
                "package": self.package.pk,
                "travel_date": date.today() + timedelta(days=7),
                "return_date": date.today() + timedelta(days=10),
                "num_travelers": 2,
                "status": "pending",
                "payment_status": "unpaid",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Notification.objects.filter(user=self.user).count(), 1)
        self.assertEqual(Notification.objects.filter(user=self.other_user).count(), 1)
        actor_message = Notification.objects.filter(user=self.user).first().message
        other_message = Notification.objects.filter(user=self.other_user).first().message
        self.assertNotIn("Updated by", actor_message)
        self.assertIn("Updated by agent2 (@agent2).", other_message)

    def test_mark_notification_as_read(self):
        notification = Notification.objects.create(
            user=self.user, title="Test", message="Message"
        )
        self.client.login(username="agent2", password="secure-pass-123")
        response = self.client.get(reverse("notification_mark_read", args=[notification.pk]))
        self.assertEqual(response.status_code, 302)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)


class RolePermissionsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.superuser = User.objects.create_user(
            username="root", password="secure-pass-123", is_superuser=True, is_staff=True
        )
        self.manager = User.objects.create_user(
            username="manager1", password="secure-pass-123"
        )
        assign_role(self.manager, "manager")
        self.normal = User.objects.create_user(
            username="user1", password="secure-pass-123"
        )
        assign_role(self.normal, "normal")
        self.other_manager = User.objects.create_user(
            username="manager2", password="secure-pass-123"
        )
        assign_role(self.other_manager, "manager")
        self.other_normal = User.objects.create_user(
            username="user2", password="secure-pass-123"
        )
        assign_role(self.other_normal, "normal")

    def test_normal_user_cannot_modify_dashboard_data(self):
        self.client.login(username="user1", password="secure-pass-123")
        response = self.client.get(reverse("package_create"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"))

    def test_manager_can_modify_dashboard_data(self):
        self.client.login(username="manager1", password="secure-pass-123")
        response = self.client.get(reverse("package_create"))
        self.assertEqual(response.status_code, 200)

    def test_normal_user_cannot_open_user_management(self):
        self.client.login(username="user1", password="secure-pass-123")
        response = self.client.get(reverse("users_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"))

    def test_manager_can_open_user_management(self):
        self.client.login(username="manager1", password="secure-pass-123")
        response = self.client.get(reverse("users_list"))
        self.assertEqual(response.status_code, 200)

    def test_manager_cannot_modify_other_manager(self):
        self.client.login(username="manager1", password="secure-pass-123")
        response = self.client.get(reverse("user_edit", args=[self.other_manager.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"))

    def test_manager_can_modify_normal_user(self):
        self.client.login(username="manager1", password="secure-pass-123")
        response = self.client.post(
            reverse("user_edit", args=[self.other_normal.pk]),
            {
                "username": "user2-updated",
                "first_name": "U",
                "last_name": "Two",
                "email": "user2@example.com",
                "role": "normal",
                "password": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))
        self.other_normal.refresh_from_db()
        self.assertEqual(self.other_normal.username, "user2-updated")

    def test_superuser_can_create_manager(self):
        self.client.login(username="root", password="secure-pass-123")
        response = self.client.post(
            reverse("user_create"),
            {
                "username": "manager3",
                "first_name": "M",
                "last_name": "Three",
                "email": "manager3@example.com",
                "password1": "strong-pass-1234",
                "password2": "strong-pass-1234",
                "role": "manager",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("users_list"))
        created_user = get_user_model().objects.get(username="manager3")
        self.assertTrue(created_user.groups.filter(name=MANAGER_GROUP_NAME).exists())

    def test_normal_user_can_view_own_profile_only(self):
        self.client.login(username="user1", password="secure-pass-123")
        own_response = self.client.get(reverse("user_profile", args=[self.normal.pk]))
        self.assertEqual(own_response.status_code, 200)
        other_response = self.client.get(
            reverse("user_profile", args=[self.other_normal.pk])
        )
        self.assertEqual(other_response.status_code, 302)
        self.assertRedirects(other_response, reverse("dashboard"))


class DashboardFeatureTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.manager = User.objects.create_user(
            username="manager-feature", password="secure-pass-123"
        )
        assign_role(self.manager, "manager")
        self.normal = User.objects.create_user(
            username="normal-feature", password="secure-pass-123"
        )
        assign_role(self.normal, "normal")
        self.destination = Destination.objects.create(
            name="Casablanca",
            country="Morocco",
            description="Coastal city package",
        )
        self.package = Package.objects.create(
            title="Casablanca Weekender",
            destination=self.destination,
            category="city_break",
            description="2 nights trip",
            duration_days=2,
            price_per_person=1200,
            max_capacity=15,
            status="active",
        )
        self.client_profile = Client.objects.create(
            first_name="Nora",
            last_name="Bennani",
            email="nora@example.com",
            phone="+212611111111",
        )
        self.guide = Guide.objects.create(
            name="Yassine Guide",
            email="yassine.guide@example.com",
            phone="+212622222222",
            languages="English,French",
            specialties="City tours",
        )
        self.booking = Booking.objects.create(
            client=self.client_profile,
            package=self.package,
            travel_date=date.today() + timedelta(days=5),
            return_date=date.today() + timedelta(days=7),
            num_travelers=2,
            total_price=2400,
            status="pending",
            payment_status="unpaid",
        )

    def test_dashboard_and_notifications_views_are_accessible(self):
        self.client.login(username="normal-feature", password="secure-pass-123")
        dashboard = self.client.get(reverse("dashboard"))
        notifications = self.client.get(reverse("notifications_list"))
        self.assertEqual(dashboard.status_code, 200)
        self.assertEqual(notifications.status_code, 200)

    def test_admin_control_requires_data_management_permission(self):
        self.client.login(username="normal-feature", password="secure-pass-123")
        denied = self.client.get(reverse("admin_control_dashboard"))
        self.assertEqual(denied.status_code, 302)
        self.assertRedirects(denied, reverse("dashboard"))

        self.client.login(username="manager-feature", password="secure-pass-123")
        allowed = self.client.get(reverse("admin_control_dashboard"))
        self.assertEqual(allowed.status_code, 200)

    def test_package_crud_flow(self):
        self.client.login(username="manager-feature", password="secure-pass-123")
        create = self.client.post(
            reverse("package_create"),
            {
                "title": "Fes Discovery",
                "destination": self.destination.pk,
                "category": "cultural",
                "description": "Historic medina tour",
                "duration_days": 3,
                "price_per_person": 900,
                "max_capacity": 20,
                "status": "active",
            },
        )
        self.assertEqual(create.status_code, 302)
        created = Package.objects.get(title="Fes Discovery")

        edit = self.client.post(
            reverse("package_edit", args=[created.pk]),
            {
                "title": "Fes Discovery Plus",
                "destination": self.destination.pk,
                "category": "cultural",
                "description": "Historic medina tour extended",
                "duration_days": 4,
                "price_per_person": 950,
                "max_capacity": 25,
                "status": "active",
            },
        )
        self.assertEqual(edit.status_code, 302)
        created.refresh_from_db()
        self.assertEqual(created.title, "Fes Discovery Plus")

    def test_client_crud_flow(self):
        self.client.login(username="manager-feature", password="secure-pass-123")
        create = self.client.post(
            reverse("client_create"),
            {
                "first_name": "Imane",
                "last_name": "Safi",
                "email": "imane@example.com",
                "phone": "+212633333333",
            },
        )
        self.assertEqual(create.status_code, 302)
        created = Client.objects.get(email="imane@example.com")

        detail = self.client.get(reverse("client_detail", args=[created.pk]))
        self.assertEqual(detail.status_code, 200)

        edit = self.client.post(
            reverse("client_edit", args=[created.pk]),
            {
                "first_name": "Imane",
                "last_name": "Safi Updated",
                "email": "imane@example.com",
                "phone": "+212633333333",
            },
        )
        self.assertEqual(edit.status_code, 302)
        created.refresh_from_db()
        self.assertEqual(created.last_name, "Safi Updated")

        delete = self.client.get(reverse("client_delete", args=[created.pk]))
        self.assertEqual(delete.status_code, 302)
        self.assertFalse(Client.objects.filter(pk=created.pk).exists())

    def test_booking_crud_flow(self):
        self.client.login(username="manager-feature", password="secure-pass-123")
        create = self.client.post(
            reverse("booking_create"),
            {
                "client": self.client_profile.pk,
                "package": self.package.pk,
                "travel_date": date.today() + timedelta(days=9),
                "return_date": date.today() + timedelta(days=12),
                "num_travelers": 3,
                "status": "pending",
                "payment_status": "unpaid",
            },
        )
        self.assertEqual(create.status_code, 302)
        created = Booking.objects.exclude(pk=self.booking.pk).get()
        self.assertEqual(float(created.total_price), 3600.0)

        edit = self.client.post(
            reverse("booking_edit", args=[created.pk]),
            {
                "client": self.client_profile.pk,
                "package": self.package.pk,
                "travel_date": date.today() + timedelta(days=10),
                "return_date": date.today() + timedelta(days=13),
                "num_travelers": 2,
                "total_price": 2400,
                "status": "confirmed",
                "payment_status": "paid",
            },
        )
        self.assertEqual(edit.status_code, 302)
        created.refresh_from_db()
        self.assertEqual(created.status, "confirmed")

    def test_destination_and_guide_crud_flows(self):
        self.client.login(username="manager-feature", password="secure-pass-123")
        dest_create = self.client.post(
            reverse("destination_create"),
            {
                "name": "Tangier",
                "country": "Morocco",
                "description": "North coast city",
                "is_featured": "on",
            },
        )
        self.assertEqual(dest_create.status_code, 302)
        created_dest = Destination.objects.get(name="Tangier")

        guide_create = self.client.post(
            reverse("guide_create"),
            {
                "name": "Salma Guide",
                "email": "salma.guide@example.com",
                "phone": "+212644444444",
                "languages": "Arabic,English",
                "specialties": "History",
                "is_available": "on",
            },
        )
        self.assertEqual(guide_create.status_code, 302)
        created_guide = Guide.objects.get(email="salma.guide@example.com")

        dest_delete = self.client.get(reverse("destination_delete", args=[created_dest.pk]))
        guide_delete = self.client.get(reverse("guide_delete", args=[created_guide.pk]))
        self.assertEqual(dest_delete.status_code, 302)
        self.assertEqual(guide_delete.status_code, 302)
        self.assertFalse(Destination.objects.filter(pk=created_dest.pk).exists())
        self.assertFalse(Guide.objects.filter(pk=created_guide.pk).exists())


class BDDScenariosTests(TestCase):
    def test_scenario_manager_creates_package_then_everyone_gets_update_notification(self):
        # Given a manager user, another normal user, and an available destination
        User = get_user_model()
        manager = User.objects.create_user(username="bdd-manager", password="secure-pass-123")
        viewer = User.objects.create_user(username="bdd-viewer", password="secure-pass-123")
        assign_role(manager, "manager")
        assign_role(viewer, "normal")
        destination = Destination.objects.create(
            name="Agadir",
            country="Morocco",
            description="Beach destination",
        )

        # When the manager creates a package from the dashboard
        self.client.login(username="bdd-manager", password="secure-pass-123")
        response = self.client.post(
            reverse("package_create"),
            {
                "title": "Agadir Escape",
                "destination": destination.pk,
                "category": "leisure",
                "description": "Relaxing beach stay",
                "duration_days": 4,
                "price_per_person": 1500,
                "max_capacity": 18,
                "status": "active",
            },
        )

        # Then the package is created and both users receive a notification
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Package.objects.filter(title="Agadir Escape").exists())
        self.assertEqual(Notification.objects.filter(user=manager).count(), 1)
        self.assertEqual(Notification.objects.filter(user=viewer).count(), 1)
        self.assertIn(
            "Updated by bdd-manager (@bdd-manager).",
            Notification.objects.filter(user=viewer).first().message,
        )

    def test_scenario_saved_profile_quick_login_without_password(self):
        # Given a registered user who has logged in once
        User = get_user_model()
        user = User.objects.create_user(username="bdd-agent", password="secure-pass-123")
        self.client.post(
            reverse("login"),
            {"username": "bdd-agent", "password": "secure-pass-123"},
        )

        # When the user logs out and then selects the saved profile
        logout_response = self.client.post(reverse("logout"))
        token = logout_response.context["recent_profiles"][0]["token"]
        login_response = self.client.post(reverse("saved_profile_login"), {"token": token})

        # Then the user is signed in again without typing the password
        self.assertEqual(login_response.status_code, 302)
        self.assertRedirects(login_response, reverse("dashboard"))
        self.assertEqual(str(self.client.session["_auth_user_id"]), str(user.pk))

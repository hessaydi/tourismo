import json

from behave import given, then, when
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from agency.models import Destination, Notification, Package
from agency.permissions import assign_role
from agency.views import RECENT_PROFILES_COOKIE


@given('a user "{username}" with password "{password}"')
def step_create_user(context, username, password):
    User = get_user_model()
    User.objects.create_user(username=username, password=password)
    context.client = Client()


@given('a manager user "{manager_username}" and a normal user "{viewer_username}"')
def step_create_manager_and_viewer(context, manager_username, viewer_username):
    User = get_user_model()
    manager = User.objects.create_user(username=manager_username, password="secure-pass-123")
    viewer = User.objects.create_user(username=viewer_username, password="secure-pass-123")
    assign_role(manager, "manager")
    assign_role(viewer, "normal")
    context.client = Client()


@given('a destination named "{name}"')
def step_create_destination(context, name):
    context.destination = Destination.objects.create(
        name=name,
        country="Morocco",
        description=f"{name} destination",
    )


@when('I login as "{username}" with password "{password}"')
def step_login(context, username, password):
    response = context.client.post(
        reverse("login"),
        {"username": username, "password": password},
    )
    assert response.status_code == 302


@when("I logout from my account")
def step_logout(context):
    response = context.client.post(reverse("logout"))
    assert response.status_code == 200


@when("I login using the first saved profile token")
def step_saved_profile_login(context):
    cookie = context.client.cookies.get(RECENT_PROFILES_COOKIE)
    assert cookie is not None and cookie.value
    profiles = json.loads(cookie.value)
    token = profiles[0]["token"]
    response = context.client.post(reverse("saved_profile_login"), {"token": token})
    assert response.status_code == 302


@when('I create a package titled "{title}"')
def step_create_package(context, title):
    response = context.client.post(
        reverse("package_create"),
        {
            "title": title,
            "destination": context.destination.pk,
            "category": "adventure",
            "description": "Scenario package",
            "duration_days": 4,
            "price_per_person": 1300,
            "max_capacity": 25,
            "status": "active",
        },
    )
    assert response.status_code == 302


@then('I should be authenticated as "{username}"')
def step_assert_authenticated_user(context, username):
    User = get_user_model()
    expected = User.objects.get(username=username)
    assert str(context.client.session.get("_auth_user_id")) == str(expected.pk)


@then('the package "{title}" should exist')
def step_assert_package_exists(context, title):
    assert Package.objects.filter(title=title).exists()


@then('user "{username}" should have {count:d} notification')
def step_assert_user_notifications_count(context, username, count):
    user = get_user_model().objects.get(username=username)
    assert Notification.objects.filter(user=user).count() == count


@then('notification for "{username}" should mention "{snippet}"')
def step_assert_notification_contains(context, username, snippet):
    user = get_user_model().objects.get(username=username)
    notification = Notification.objects.filter(user=user).first()
    assert notification is not None
    assert snippet in notification.message

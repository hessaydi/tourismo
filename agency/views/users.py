from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from ..permissions import (
    NORMAL_ROLE,
    assign_role,
    can_modify_user,
    can_view_user,
    get_user_role,
    role_choices_for_actor,
)
from .shared import _forbidden_redirect, require_user_management


@require_user_management
def users_list(request):
    User = get_user_model()
    users = User.objects.order_by("username")

    if not request.user.is_superuser:
        users = users.filter(is_superuser=False)

    user_rows = [
        {
            "obj": user_obj,
            "role": get_user_role(user_obj),
            "editable": can_modify_user(request.user, user_obj),
        }
        for user_obj in users
    ]

    return render(
        request,
        "agency/users.html",
        {
            "user_rows": user_rows,
            "is_superuser_view": request.user.is_superuser,
        },
    )


def user_profile(request, pk):
    User = get_user_model()
    user_obj = get_object_or_404(User, pk=pk)
    if not can_view_user(request.user, user_obj):
        return _forbidden_redirect(request, "You are not allowed to view this profile.")

    return render(
        request,
        "agency/user_profile.html",
        {
            "profile_user": user_obj,
            "can_modify_profile_user": can_modify_user(request.user, user_obj),
            "profile_role": get_user_role(user_obj),
        },
    )


@require_user_management
def user_create(request):
    allowed_roles = role_choices_for_actor(request.user)
    if not allowed_roles:
        return _forbidden_redirect(request, "You do not have permission to create users.")

    roles = {role for role, _ in allowed_roles}
    selected_role = NORMAL_ROLE
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        selected_role = request.POST.get("role", NORMAL_ROLE)
        if selected_role not in roles:
            form.add_error(None, "Selected role is not allowed for your account.")
        if form.is_valid():
            user = form.save()
            user.first_name = request.POST.get("first_name", "").strip()
            user.last_name = request.POST.get("last_name", "").strip()
            user.email = request.POST.get("email", "").strip()
            user.save(update_fields=["first_name", "last_name", "email"])
            assign_role(user, selected_role)
            messages.success(request, f"User {user.username} created successfully.")
            return redirect("users_list")
    else:
        form = UserCreationForm()

    return render(
        request,
        "agency/user_form.html",
        {
            "form": form,
            "role_choices": allowed_roles,
            "selected_role": selected_role,
            "is_create": True,
            "post_first_name": request.POST.get("first_name", ""),
            "post_last_name": request.POST.get("last_name", ""),
            "post_email": request.POST.get("email", ""),
        },
    )


@require_user_management
def user_edit(request, pk):
    User = get_user_model()
    user_obj = get_object_or_404(User, pk=pk)
    if not can_modify_user(request.user, user_obj):
        return _forbidden_redirect(request, "You cannot modify this user.")

    allowed_roles = role_choices_for_actor(request.user)
    roles = {role for role, _ in allowed_roles}
    selected_role = get_user_role(user_obj)

    if request.method == "POST":
        user_obj.username = request.POST.get("username", "").strip()
        user_obj.first_name = request.POST.get("first_name", "").strip()
        user_obj.last_name = request.POST.get("last_name", "").strip()
        user_obj.email = request.POST.get("email", "").strip()
        selected_role = request.POST.get("role", NORMAL_ROLE)
        password = request.POST.get("password", "").strip()

        if not user_obj.username:
            messages.error(request, "Username is required.")
        elif (
            User.objects.exclude(pk=user_obj.pk).filter(username=user_obj.username).exists()
        ):
            messages.error(request, "Username is already taken.")
        elif selected_role not in roles:
            messages.error(request, "You are not allowed to assign that role.")
        else:
            user_obj.save()
            assign_role(user_obj, selected_role)
            if password:
                user_obj.set_password(password)
                user_obj.save(update_fields=["password"])
            messages.success(request, f"User {user_obj.username} updated successfully.")
            return redirect("users_list")

    return render(
        request,
        "agency/user_form.html",
        {
            "edit_user": user_obj,
            "role_choices": allowed_roles,
            "selected_role": selected_role,
            "is_create": False,
        },
    )


@require_user_management
def user_delete(request, pk):
    User = get_user_model()
    user_obj = get_object_or_404(User, pk=pk)
    if not can_modify_user(request.user, user_obj):
        return _forbidden_redirect(request, "You cannot delete this user.")
    username = user_obj.username
    user_obj.delete()
    messages.success(request, f"User {username} deleted successfully.")
    return redirect("users_list")

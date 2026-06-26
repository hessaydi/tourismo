from django.contrib.auth.models import Group

MANAGER_ROLE = "manager"
NORMAL_ROLE = "normal"
SUPERUSER_ROLE = "superuser"
MANAGER_GROUP_NAME = "Managers"


def is_manager(user) -> bool:
    if not user.is_authenticated or user.is_superuser:
        return False
    return user.groups.filter(name=MANAGER_GROUP_NAME).exists()


def get_user_role(user) -> str:
    if not user.is_authenticated:
        return NORMAL_ROLE
    if user.is_superuser:
        return SUPERUSER_ROLE
    if is_manager(user):
        return MANAGER_ROLE
    return NORMAL_ROLE


def can_manage_dashboard_data(user) -> bool:
    return user.is_authenticated and (user.is_superuser or is_manager(user))


def can_manage_users(user) -> bool:
    return can_manage_dashboard_data(user)


def can_view_user(actor, target) -> bool:
    if not actor.is_authenticated:
        return False
    if actor.is_superuser:
        return True
    if is_manager(actor):
        return not target.is_superuser
    return actor.pk == target.pk


def can_modify_user(actor, target) -> bool:
    if not actor.is_authenticated:
        return False
    if actor.is_superuser:
        return actor.pk != target.pk
    if is_manager(actor):
        return (
            actor.pk != target.pk
            and not target.is_superuser
            and not is_manager(target)
        )
    return False


def assign_role(user, role: str) -> None:
    manager_group, _ = Group.objects.get_or_create(name=MANAGER_GROUP_NAME)

    if role == SUPERUSER_ROLE:
        user.is_superuser = True
        user.is_staff = True
        user.save(update_fields=["is_superuser", "is_staff"])
        user.groups.remove(manager_group)
        return

    user.is_superuser = False
    user.is_staff = False
    user.save(update_fields=["is_superuser", "is_staff"])

    if role == MANAGER_ROLE:
        user.groups.add(manager_group)
    else:
        user.groups.remove(manager_group)


def role_choices_for_actor(actor):
    if actor.is_superuser:
        return [
            (SUPERUSER_ROLE, "Superuser"),
            (MANAGER_ROLE, "Manager"),
            (NORMAL_ROLE, "Normal user"),
        ]
    if is_manager(actor):
        return [(NORMAL_ROLE, "Normal user")]
    return []

from .permissions import can_manage_dashboard_data, can_manage_users, get_user_role


def notifications_context(request):
    if not request.user.is_authenticated:
        return {
            "recent_notifications": [],
            "unread_notifications_count": 0,
            "can_manage_data": False,
            "can_manage_users": False,
            "user_role": "normal",
        }

    notifications = request.user.notifications.all()
    return {
        "recent_notifications": notifications[:5],
        "unread_notifications_count": notifications.filter(is_read=False).count(),
        "can_manage_data": can_manage_dashboard_data(request.user),
        "can_manage_users": can_manage_users(request.user),
        "user_role": get_user_role(request.user),
    }

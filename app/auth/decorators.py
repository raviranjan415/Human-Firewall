"""Shared authorisation helpers.

Permissions are enforced on the server. Hiding a button in a template is a
convenience, never a control.
"""

from functools import wraps

from flask import abort, jsonify, request
from flask_login import current_user, login_required

from app.models.user import ROLE_ADMIN, ROLE_INSTRUCTOR, ROLE_LEARNER


def role_required(*roles: str):
    """Allow only the given roles. Everyone else gets 403 (or JSON for /api)."""

    def decorator(view):
        @wraps(view)
        @login_required
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role_name not in roles:
                if request.path.startswith("/api/"):
                    return jsonify({"error": "forbidden", "message": "Not permitted"}), 403
                abort(403)
            return view(*args, **kwargs)

        return wrapper

    return decorator


admin_required = role_required(ROLE_ADMIN)
instructor_required = role_required(ROLE_ADMIN, ROLE_INSTRUCTOR)
learner_or_higher = role_required(ROLE_ADMIN, ROLE_INSTRUCTOR, ROLE_LEARNER)


def org_admin_required(view):
    """Require Platform Admin or Organization Administrator / T&P Coordinator permissions."""
    @wraps(view)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)
        if current_user.is_admin:
            return view(*args, **kwargs)

        org_id = kwargs.get("org_id")
        if org_id:
            if not current_user.is_org_admin_for(int(org_id)):
                abort(403)
        elif not current_user.is_org_admin:
            abort(403)
        return view(*args, **kwargs)

    return wrapper


def tenant_membership_required(view):
    """Ensure learner or admin has an active membership in the requested organization workspace."""
    @wraps(view)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)
        if current_user.is_admin:
            return view(*args, **kwargs)

        org_id = kwargs.get("org_id")
        if org_id:
            membership = current_user.get_membership(int(org_id))
            if not membership or membership.status != "active":
                abort(403)
        return view(*args, **kwargs)

    return wrapper


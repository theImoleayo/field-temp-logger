# -------------------------------------------------
# auth.py (simple session auth)
# -------------------------------------------------
from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('admin_user'):
            flash('Please log in to access the dashboard.', 'warning')
            return redirect(url_for('views.login'))
        return view(*args, **kwargs)
    return wrapped
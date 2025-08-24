# -------------------------------------------------
# views.py (web views + JSON for dashboard)
# -------------------------------------------------
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash
from database import db
from models import Admin, DailyCheckin, Reading, today_date_str
from auth import login_required
from sqlalchemy import func, desc
from datetime import datetime
from pytz import timezone
from config import Config


bp_views = Blueprint('views', __name__)
TZ = timezone(Config.TIMEZONE)


@bp_views.get('/')
@login_required
def root():
    return redirect(url_for('views.dashboard'))


@bp_views.get('/login')
def login():
    return render_template('login.html')


@bp_views.post('/login')
def login_post():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    admin = Admin.query.filter_by(username=username).first()
    if not admin or not check_password_hash(admin.password_hash, password):
        flash('Invalid credentials', 'danger')
        return redirect(url_for('views.login'))
    session['admin_user'] = username
    return redirect(url_for('views.dashboard'))


@bp_views.get('/logout')
@login_required
def logout():
    session.pop('admin_user', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('views.login'))


@bp_views.get('/dashboard')
@login_required
def dashboard():
    """Admin dashboard showing today's registered workers."""
    date_str = today_date_str()
    checkins = DailyCheckin.query.filter_by(date_str=date_str).all()
    return render_template('dashboard.html', checkins=checkins, date_str=date_str)


@bp_views.get('/checkin')
def checkin():
    """Public check-in page (no auth required)."""
    return render_template('checkin.html')


@bp_views.post('/checkin')
def checkin_post():
    """Handle worker check-in form submission."""
    full_name = request.form.get('full_name', '').strip()
    worker_id = request.form.get('worker_id', '').strip()
    element_id = request.form.get('element_id', '').strip()
    
    if not all([full_name, worker_id, element_id]):
        flash('All fields are required.', 'danger')
        return redirect(url_for('views.checkin'))
    
    date_str = today_date_str()
    
    # Check if worker already checked in today
    existing = DailyCheckin.query.filter_by(date_str=date_str, worker_id=worker_id).first()
    if existing:
        flash(f'Worker {worker_id} already checked in today.', 'warning')
        return redirect(url_for('views.checkin'))
    
    # Check if element_id is already taken today
    existing_element = DailyCheckin.query.filter_by(date_str=date_str, element_id=element_id).first()
    if existing_element:
        flash(f'Element ID {element_id} is already taken today.', 'danger')
        return redirect(url_for('views.checkin'))
    
    # Create check-in record
    checkin = DailyCheckin(
        date_str=date_str,
        worker_id=worker_id,
        full_name=full_name,
        element_id=element_id
    )
    db.session.add(checkin)
    db.session.commit()
    
    flash(f'Check-in successful! Worker {worker_id} registered with element {element_id}.', 'success')
    return redirect(url_for('views.checkin'))


@bp_views.get('/api/today/latest')
def api_today_latest():
    """API endpoint for dashboard to fetch latest temperature readings."""
    date_str = today_date_str()
    checkins = DailyCheckin.query.filter_by(date_str=date_str).all()
    
    result = {}
    for checkin in checkins:
        # Get the most recent reading for this element_id
        latest_reading = Reading.query.filter_by(element_id=checkin.element_id).order_by(desc(Reading.recorded_at)).first()
        
        if latest_reading:
            # Convert UTC to local time
            recorded_local = latest_reading.recorded_at.replace(tzinfo=timezone('UTC')).astimezone(TZ)
            result[checkin.worker_id] = {
                'temperature_c': latest_reading.temperature_c,
                'recorded_local': recorded_local.strftime('%H:%M:%S')
            }
        else:
            result[checkin.worker_id] = {
                'temperature_c': None,
                'recorded_local': None
            }
    
    return jsonify(result)

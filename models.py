# -------------------------------------------------
# models.py
# -------------------------------------------------
from datetime import datetime
from database import db
from pytz import timezone
from config import Config


TZ = timezone(Config.TIMEZONE)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


class DailyCheckin(db.Model):
    __tablename__ = 'daily_checkins'
    id = db.Column(db.Integer, primary_key=True)
    date_str = db.Column(db.String(10), index=True, nullable=False) # YYYY-MM-DD in Africa/Lagos
    worker_id = db.Column(db.String(64), index=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    element_id = db.Column(db.String(64), index=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Reading(db.Model):
    __tablename__ = 'readings'
    id = db.Column(db.Integer, primary_key=True)
    element_id = db.Column(db.String(64), index=True, nullable=False)
    temperature_c = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, index=True, default=datetime.utcnow) # UTC


    def to_dict(self):
        return {
            'element_id': self.element_id,
            'temperature_c': self.temperature_c,
            'recorded_at': self.recorded_at.isoformat() + 'Z',
        }


# Helpers


def today_date_str():
    now_local = datetime.now(TZ)
    return now_local.strftime('%Y-%m-%d')
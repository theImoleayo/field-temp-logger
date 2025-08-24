# -------------------------------------------------
# seed_admin.py (create initial admin from .env)
# -------------------------------------------------
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from app import create_app
from database import db
from models import Admin


load_dotenv()


app = create_app()
with app.app_context():
    username = os.getenv('ADMIN_USERNAME', 'admin')
    password = os.getenv('ADMIN_PASSWORD', 'admin123')
    if not Admin.query.filter_by(username=username).first():
        admin = Admin(username=username, password_hash=generate_password_hash(password))
        db.session.add(admin)
        db.session.commit()
        print(f'Admin user created: {username}')
    else:
        print('Admin user already exists.')

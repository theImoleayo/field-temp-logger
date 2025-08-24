# -------------------------------------------------
# app.py (app factory + blueprint register)
# -------------------------------------------------
from flask import Flask
from config import Config
from database import db
from views import bp_views
from ingest import bp_ingest




def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)


    db.init_app(app)


# Register blueprints
    app.register_blueprint(bp_views)
    app.register_blueprint(bp_ingest)


# Ensure instance folder exists for SQLite
    import os
    os.makedirs(app.instance_path, exist_ok=True)


    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

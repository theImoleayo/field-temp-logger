# -------------------------------------------------
# config.py
# -------------------------------------------------
import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    # Fix SQLite path to be absolute
    DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance", "app.db")
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL", f"sqlite:///{DEFAULT_DB_PATH}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIMEZONE = "Africa/Lagos"
    INGEST_API_KEY = os.getenv("INGEST_API_KEY")
    
    # ThingSpeak API Configuration
    THINGSPEAK_READ_API_KEY = os.getenv("THINGSPEAK_READ_API_KEY", "YKWSHBBTJZP4EZ46")
    THINGSPEAK_WRITE_API_KEY = os.getenv("THINGSPEAK_WRITE_API_KEY", "RAPODLW686AVLMSN")
    THINGSPEAK_SERVER = "api.thingspeak.com"

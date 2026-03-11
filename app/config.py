import os
from dotenv import load_dotenv

# Load local .env file if it exists (Render will ignore this and use its dashboard variables)
load_dotenv()

class Config:
    """Base configuration."""
    # Other base settings like SECRET_KEY or Rate Limiter defaults
    RATELIMIT_DEFAULT = "200 per day; 50 per hour"

class DevelopmentConfig(Config):
    """Local machine configuration."""
    DEBUG = True
    # Uses local Redis by default
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class TestingConfig(Config):
    """Pytest configuration."""
    TESTING = True
    # Force tests to use a completely separate Redis database (e.g., DB 1 instead of DB 0)
    # This prevents test pollution from wiping out your local development cache
    REDIS_URL = os.getenv("TEST_REDIS_URL", "redis://localhost:6379/1")

class ProductionConfig(Config):
    """Render production configuration."""
    DEBUG = False
    # In production, there is no fallback string. It MUST exist in the Render environment.
    REDIS_URL = os.environ.get("REDIS_URL")
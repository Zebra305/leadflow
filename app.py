import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database connection
# Use the provided PostgreSQL credentials
database_url = (
    f"postgresql://{os.environ.get('PGUSER', 'readonly_user')}:"
    f"{os.environ.get('PGPASSWORD', 'a_very_strong_password')}@"
    f"{os.environ.get('PGHOST', '69.62.114.108')}:"
    f"{os.environ.get('PGPORT', '5432')}/"
    f"{os.environ.get('PGDATABASE', 'n8n_outreach')}"
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", database_url)
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models and routes
    import models
    import routes
    
    # Create tables if they don't exist
    db.create_all()

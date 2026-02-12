import os
import logging
from flask import Flask
from mongoengine import connect
from flask_login import LoginManager

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Configure session to expire on browser close only
from datetime import timedelta
app.config["SESSION_PERMANENT"] = False  # Session expires when browser closes
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_REFRESH_EACH_REQUEST"] = True  # Keep session alive during use

# Configure MongoDB Atlas connection
MONGODB_URI = ' '

# Connect to MongoDB with more lenient settings
db = connect(
    db='exam_evaluator',
    host=MONGODB_URI,
    maxPoolSize=10,
    minPoolSize=1,
    serverSelectionTimeoutMS=30000,
    socketTimeoutMS=60000,
    connectTimeoutMS=30000,
    connect=False,  # Lazy connection
)

# Ensure instance directory exists
instance_path = os.path.join(os.getcwd(), 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path, mode=0o777)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max-limit


# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = "strong"  # Strong session protection
login_manager.refresh_view = 'auth.login'

# Create required directories
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs("instance", exist_ok=True)

# Register blueprints
from auth import auth_bp
app.register_blueprint(auth_bp)

from routes.exam_routes import exam_bp
app.register_blueprint(exam_bp)

from routes.report_routes import report_bp
app.register_blueprint(report_bp)

from routes.file_routes import file_bp
app.register_blueprint(file_bp)

from routes.database_routes import database_bp
app.register_blueprint(database_bp)

from routes.student_routes import student_bp
app.register_blueprint(student_bp)

# Add favicon route
@app.route('/favicon.ico')
def favicon():
    return '', 204

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from models import User
    try:
        return User.objects(id=user_id).first()
    except:
        return None

# Test MongoDB connection - with timeout
# Commented out to allow app to start even if MongoDB is slow
# with app.app_context():
#     try:
#         from models import User
#         # Simple query to test connection
#         User.objects().first()
#         logging.info("MongoDB connection successful!")
#     except Exception as e:
#         logging.error(f"MongoDB connection error: {e}")

# Force debug mode ON
app.debug = True
app.config['DEBUG'] = True

# Global error handler to print all exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    print('GLOBAL ERROR:', e)
    traceback.print_exc()
    return f"<pre>Internal Server Error\n{e}\n{traceback.format_exc()}</pre>", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


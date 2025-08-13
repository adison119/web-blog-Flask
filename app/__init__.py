from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"

    # filters
    from .filters import nl2br, render_markdown
    app.jinja_env.filters['nl2br'] = nl2br
    app.jinja_env.filters['md'] = render_markdown

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    from .models import User, Post, Setting  # noqa: F401
    from .routes import main_bp
    from .auth import auth_bp
    from .admin import admin_bp

    # global settings in templates
    @app.context_processor
    def inject_settings():
        from .models import Setting
        s = db.session.query(Setting).first()
        return dict(settings=s)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        db.create_all()
        from .models import Setting
        if db.session.query(Setting).count() == 0:
            db.session.add(Setting(site_title="My Blog", site_tagline="Powered by Flask", layout="right", primary_color="#3b82f6"))
            db.session.commit()

    return app

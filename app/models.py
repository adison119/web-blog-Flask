from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from sqlalchemy import func

class User(UserMixin, db.Model):
    id = db.mapped_column(db.Integer, primary_key=True)
    username = db.mapped_column(db.String(80), unique=True, nullable=False)
    email = db.mapped_column(db.String(120), unique=True, nullable=False)
    password_hash = db.mapped_column(db.String(256), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class Post(db.Model):
    id = db.mapped_column(db.Integer, primary_key=True)
    title = db.mapped_column(db.String(200), nullable=False)
    content = db.mapped_column(db.Text, nullable=False)
    created_at = db.mapped_column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.mapped_column(db.DateTime(timezone=True), onupdate=func.now())
    author_id = db.mapped_column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    image_filename = db.mapped_column(db.String(255), nullable=True)  # cover image

class Setting(db.Model):
    id = db.mapped_column(db.Integer, primary_key=True)
    site_title = db.mapped_column(db.String(120), default="My Blog")
    site_tagline = db.mapped_column(db.String(200), default="Powered by Flask")
    layout = db.mapped_column(db.String(10), default="right")  # 'left' or 'right'
    primary_color = db.mapped_column(db.String(9), default="#3b82f6")

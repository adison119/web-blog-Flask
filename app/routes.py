from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import current_user, login_required
from . import db
from .models import Post, Setting

from werkzeug.utils import secure_filename
import uuid, os

main_bp = Blueprint("main", __name__)

def _allowed_image(filename):
    ALLOWED = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    ext = ('.' + filename.rsplit('.', 1)[-1].lower()) if '.' in filename else ''
    return ext in ALLOWED

def _save_image(file_storage):
    if not file_storage or file_storage.filename.strip() == '':
        return None
    if not _allowed_image(file_storage.filename):
        flash("ไฟล์รูปภาพไม่รองรับ (อนุญาต: png, jpg, jpeg, gif, webp)", "danger")
        return None
    fn = secure_filename(file_storage.filename)
    ext = '.' + fn.rsplit('.', 1)[-1].lower()
    new_name = f"{uuid.uuid4().hex}{ext}"
    dest = os.path.join(current_app.config['UPLOAD_FOLDER'], new_name)
    file_storage.save(dest)
    return new_name

def _delete_image(filename):
    if not filename:
        return
    path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass

@main_bp.route("/")
def index():
    q = request.args.get("q")
    posts_query = db.session.query(Post).order_by(Post.created_at.desc())
    if q:
        posts_query = posts_query.filter(Post.title.ilike(f"%{q}%"))
    posts = posts_query.all()
    return render_template("index.html", posts=posts, q=q or "")

@main_bp.route("/post/<int:post_id>")
def post_detail(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)
    return render_template("post_detail.html", post=post)

@main_bp.route("/post/new", methods=["GET", "POST"])
@login_required
def post_new():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        img_file = request.files.get("image")
        if not title or not content:
            flash("กรุณากรอกหัวข้อและเนื้อหา", "danger")
        else:
            img_name = _save_image(img_file)
            post = Post(title=title, content=content, author_id=current_user.id, image_filename=img_name)
            db.session.add(post)
            db.session.commit()
            flash("สร้างโพสต์สำเร็จ", "success")
            return redirect(url_for("main.index"))
    return render_template("post_form.html", mode="create")

@main_bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def post_edit(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)
    if post.author_id != current_user.id:
        abort(403)
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        img_file = request.files.get("image")
        if not title or not content:
            flash("กรุณากรอกหัวข้อและเนื้อหา", "danger")
        else:
            post.title = title
            post.content = content
            new_img = _save_image(img_file)
            if new_img:
                _delete_image(post.image_filename)
                post.image_filename = new_img
            db.session.commit()
            flash("อัปเดตโพสต์สำเร็จ", "success")
            return redirect(url_for("main.post_detail", post_id=post.id))
    return render_template("post_form.html", mode="edit", post=post)

@main_bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def post_delete(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)
    if post.author_id != current_user.id:
        abort(403)
    _delete_image(post.image_filename)
    db.session.delete(post)
    db.session.commit()
    flash("ลบโพสต์แล้ว", "info")
    return redirect(url_for("main.index"))

# Inline image upload for editor
@main_bp.route("/upload/image", methods=["POST"])
@login_required
def upload_image():
    file = request.files.get("image")
    if not file:
        return {"error": "no file"}, 400
    name = _save_image(file)
    if not name:
        return {"error": "invalid file"}, 400
    return {"url": url_for('static', filename=f'uploads/{name}'), "filename": name}

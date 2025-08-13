from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    if request.method == "POST":
        username = request.form.get("username","").strip()
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        confirm = request.form.get("confirm","")
        if not username or not email or not password:
            flash("กรอกข้อมูลให้ครบ", "danger")
        elif password != confirm:
            flash("รหัสผ่านไม่ตรงกัน", "danger")
        elif db.session.query(User).filter((User.username==username)|(User.email==email)).first():
            flash("username หรือ email ถูกใช้แล้ว", "danger")
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("สมัครสมาชิกสำเร็จ! เข้าสู่ระบบได้เลย", "success")
            return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        user = db.session.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash("เข้าสู่ระบบสำเร็จ", "success")
            next_url = request.args.get("next") or url_for("main.index")
            return redirect(next_url)
        else:
            flash("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง", "danger")
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("ออกจากระบบแล้ว", "info")
    return redirect(url_for("main.index"))

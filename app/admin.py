from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .models import Setting
from . import db

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/layout", methods=["GET","POST"])
@login_required
def layout_settings():
    settings = db.session.query(Setting).first()
    if request.method == "POST":
        settings.site_title = request.form.get("site_title","My Blog")[:120]
        settings.site_tagline = request.form.get("site_tagline","")[:200]
        settings.layout = request.form.get("layout","right")
        settings.primary_color = request.form.get("primary_color","#3b82f6")
        db.session.commit()
        flash("บันทึกการตั้งค่า Layout แล้ว", "success")
        return redirect(url_for("admin.layout_settings"))
    return render_template("layout_settings.html", settings=settings)

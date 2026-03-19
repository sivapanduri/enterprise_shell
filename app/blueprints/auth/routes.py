from datetime import datetime, timezone

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.blueprints.auth import auth_bp
from app.forms.auth import LoginForm
from app.models.user import User


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()

        if user and user.is_active and user.check_password(form.password.data):
            user.last_login_at = datetime.now(timezone.utc)
            user.last_login_ip = request.headers.get(
                "X-Forwarded-For",
                request.remote_addr,
            )

            from app.extensions import db
            db.session.commit()

            login_user(user, remember=form.remember_me.data)
            flash(f"Welcome back, {user.display_name}.", "success")

            next_url = request.args.get("next")
            return redirect(next_url or url_for("dashboard.index"))

        flash("Invalid email or password.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.post("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("public.home"))
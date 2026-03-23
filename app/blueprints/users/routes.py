from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.blueprints.users import users_bp
from app.extensions import db
from app.forms.users import UserCreateForm, UserEditForm, UserRoleAssignmentForm
from app.models.rbac import Role, UserRole
from app.models.user import User
from app.security.decorators import permission_required


@users_bp.get("/")
@permission_required("users.view")
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("users/list.html", users=users)


@users_bp.route("/create", methods=["GET", "POST"])
@permission_required("users.create")
def create_user():
    form = UserCreateForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        username = form.username.data.strip()

        existing = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()
        if existing:
            flash("A user with that email or username already exists.", "danger")
            return render_template("users/create.html", form=form)

        user = User(
            email=email,
            username=username,
            first_name=form.first_name.data.strip() or None,
            last_name=form.last_name.data.strip() or None,
            is_active=form.is_active.data,
            is_superadmin=form.is_superadmin.data,
            must_change_password=form.must_change_password.data,
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("User created successfully.", "success")
        return redirect(url_for("users.detail_user", user_id=user.id))

    return render_template("users/create.html", form=form)


@users_bp.get("/<int:user_id>")
@permission_required("users.view")
def detail_user(user_id: int):
    user = User.query.get_or_404(user_id)
    return render_template("users/detail.html", user=user)


@users_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@permission_required("users.edit")
def edit_user(user_id: int):
    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        username = form.username.data.strip()

        existing = User.query.filter(
            ((User.email == email) | (User.username == username)) & (User.id != user.id)
        ).first()
        if existing:
            flash("Another user already uses that email or username.", "danger")
            return render_template("users/edit.html", form=form, user=user)

        user.email = email
        user.username = username
        user.first_name = form.first_name.data.strip() or None
        user.last_name = form.last_name.data.strip() or None
        user.is_active = form.is_active.data
        user.is_superadmin = form.is_superadmin.data
        user.must_change_password = form.must_change_password.data

        db.session.commit()

        flash("User updated successfully.", "success")
        return redirect(url_for("users.detail_user", user_id=user.id))

    return render_template("users/edit.html", form=form, user=user)


@users_bp.route("/<int:user_id>/roles", methods=["GET", "POST"])
@permission_required("users.assign_roles")
def assign_roles(user_id: int):
    user = User.query.get_or_404(user_id)
    form = UserRoleAssignmentForm()

    roles = Role.query.order_by(Role.label.asc(), Role.name.asc()).all()
    form.role_ids.choices = [(role.id, f"{role.label} ({role.name})") for role in roles]

    if request.method == "GET":
        form.role_ids.data = [user_role.role_id for user_role in user.roles]

    if form.validate_on_submit():
        selected_role_ids = set(form.role_ids.data)
        current_role_ids = {user_role.role_id for user_role in user.roles}

        for user_role in list(user.roles):
            if user_role.role_id not in selected_role_ids:
                db.session.delete(user_role)

        for role_id in selected_role_ids - current_role_ids:
            db.session.add(
                UserRole(
                    user_id=user.id,
                    role_id=role_id,
                    assigned_by_id=current_user.id,
                )
            )

        db.session.commit()
        flash("User roles updated successfully.", "success")
        return redirect(url_for("users.detail_user", user_id=user.id))

    return render_template("users/roles.html", form=form, user=user, roles=roles)


@users_bp.post("/<int:user_id>/toggle-active")
@permission_required("users.edit")
def toggle_active(user_id: int):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("You cannot deactivate your own account from this screen.", "danger")
        return redirect(url_for("users.detail_user", user_id=user.id))

    user.is_active = not user.is_active
    db.session.commit()

    state_label = "activated" if user.is_active else "deactivated"
    flash(f"User {state_label} successfully.", "success")
    return redirect(url_for("users.detail_user", user_id=user.id))
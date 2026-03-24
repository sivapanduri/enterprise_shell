from collections import defaultdict

from flask import flash, redirect, render_template, request, url_for

from app.blueprints.roles import roles_bp
from app.extensions import db
from app.forms.roles import RoleForm, RolePermissionAssignmentForm
from app.models.rbac import Permission, Role, RolePermission
from app.security.decorators import permission_required


@roles_bp.get("/")
@permission_required("roles.view")
def list_roles():
    roles = Role.query.order_by(Role.label.asc(), Role.name.asc()).all()
    return render_template("roles/list.html", roles=roles)


@roles_bp.route("/create", methods=["GET", "POST"])
@permission_required("roles.create")
def create_role():
    form = RoleForm()

    if form.validate_on_submit():
        name = form.name.data.strip()
        label = form.label.data.strip()

        existing = Role.query.filter_by(name=name).first()
        if existing:
            flash("A role with that system name already exists.", "danger")
            return render_template("roles/create.html", form=form)

        role = Role(
            name=name,
            label=label,
            description=(form.description.data or "").strip() or None,
            is_system_role=form.is_system_role.data,
        )
        db.session.add(role)
        db.session.commit()

        flash("Role created successfully.", "success")
        return redirect(url_for("roles.detail_role", role_id=role.id))

    return render_template("roles/create.html", form=form)


@roles_bp.get("/<int:role_id>")
@permission_required("roles.view")
def detail_role(role_id: int):
    role = Role.query.get_or_404(role_id)

    permission_groups = defaultdict(list)
    for role_permission in role.permissions:
        if role_permission.permission:
            permission_groups[role_permission.permission.module].append(role_permission.permission)

    permission_groups = dict(sorted(permission_groups.items(), key=lambda item: item[0].lower()))
    return render_template(
        "roles/detail.html",
        role=role,
        permission_groups=permission_groups,
    )


@roles_bp.route("/<int:role_id>/edit", methods=["GET", "POST"])
@permission_required("roles.edit")
def edit_role(role_id: int):
    role = Role.query.get_or_404(role_id)
    form = RoleForm(obj=role)

    if form.validate_on_submit():
        name = form.name.data.strip()
        label = form.label.data.strip()

        existing = Role.query.filter(
            (Role.name == name) & (Role.id != role.id)
        ).first()
        if existing:
            flash("Another role already uses that system name.", "danger")
            return render_template("roles/edit.html", form=form, role=role)

        role.name = name
        role.label = label
        role.description = (form.description.data or "").strip() or None
        role.is_system_role = form.is_system_role.data

        db.session.commit()

        flash("Role updated successfully.", "success")
        return redirect(url_for("roles.detail_role", role_id=role.id))

    return render_template("roles/edit.html", form=form, role=role)


@roles_bp.route("/<int:role_id>/permissions", methods=["GET", "POST"])
@permission_required("roles.assign_permissions")
def assign_permissions(role_id: int):
    role = Role.query.get_or_404(role_id)
    form = RolePermissionAssignmentForm()

    permissions = Permission.query.order_by(Permission.module.asc(), Permission.name.asc()).all()
    form.permission_ids.choices = [
        (permission.id, f"{permission.module} — {permission.name}")
        for permission in permissions
    ]

    if request.method == "GET":
        form.permission_ids.data = [role_permission.permission_id for role_permission in role.permissions]

    if form.validate_on_submit():
        selected_permission_ids = set(form.permission_ids.data)
        current_permission_ids = {role_permission.permission_id for role_permission in role.permissions}

        for role_permission in list(role.permissions):
            if role_permission.permission_id not in selected_permission_ids:
                db.session.delete(role_permission)

        for permission_id in selected_permission_ids - current_permission_ids:
            db.session.add(
                RolePermission(
                    role_id=role.id,
                    permission_id=permission_id,
                )
            )

        db.session.commit()
        flash("Role permissions updated successfully.", "success")
        return redirect(url_for("roles.detail_role", role_id=role.id))

    permission_groups = defaultdict(list)
    for permission in permissions:
        permission_groups[permission.module].append(permission)

    permission_groups = dict(sorted(permission_groups.items(), key=lambda item: item[0].lower()))

    return render_template(
        "roles/permissions.html",
        form=form,
        role=role,
        permission_groups=permission_groups,
    )


@roles_bp.get("/permissions")
@permission_required("permissions.view")
def permission_catalog():
    permissions = Permission.query.order_by(Permission.module.asc(), Permission.name.asc()).all()

    grouped_permissions = defaultdict(list)
    for permission in permissions:
        grouped_permissions[permission.module].append(permission)

    grouped_permissions = dict(sorted(grouped_permissions.items(), key=lambda item: item[0].lower()))
    return render_template("permissions/list.html", grouped_permissions=grouped_permissions)
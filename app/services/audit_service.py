from __future__ import annotations

from flask import has_request_context, request
from flask_login import current_user

from app.extensions import db
from app.models.audit import AuditEntry, AuditTransaction


class AuditService:
    @staticmethod
    def start_transaction(action: str, description: str | None = None) -> AuditTransaction:
        actor_id = None
        ip_address = None
        user_agent = None

        if has_request_context():
            ip_address = request.remote_addr
            user_agent = request.headers.get("User-Agent")
            if getattr(current_user, "is_authenticated", False):
                actor_id = current_user.id

        tx = AuditTransaction(
            actor_id=actor_id,
            action=action,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.session.add(tx)
        db.session.flush()
        return tx

    @staticmethod
    def add_entry(
        transaction: AuditTransaction,
        *,
        table_name: str,
        record_id: str | int | None,
        operation: str,
        before_data=None,
        after_data=None,
    ) -> AuditEntry:
        entry = AuditEntry(
            transaction_id=transaction.id,
            table_name=table_name,
            record_id=str(record_id) if record_id is not None else None,
            operation=operation,
            before_data=before_data,
            after_data=after_data,
        )
        db.session.add(entry)
        return entry

    @staticmethod
    def snapshot_user(user) -> dict:
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "is_superadmin": user.is_superadmin,
            "must_change_password": user.must_change_password,
        }

    @staticmethod
    def snapshot_role(role) -> dict:
        return {
            "id": role.id,
            "name": role.name,
            "label": role.label,
            "description": role.description,
            "is_system_role": role.is_system_role,
        }

    @staticmethod
    def snapshot_user_roles(user) -> dict:
        return {
            "user_id": user.id,
            "role_ids": sorted([user_role.role_id for user_role in user.roles]),
            "role_names": sorted(
                [user_role.role.name for user_role in user.roles if user_role.role]
            ),
        }

    @staticmethod
    def snapshot_role_permissions(role) -> dict:
        permissions = []
        for role_permission in role.permissions:
            if role_permission.permission:
                permissions.append(role_permission.permission.name)

        return {
            "role_id": role.id,
            "permission_ids": sorted([rp.permission_id for rp in role.permissions]),
            "permission_names": sorted(permissions),
        }

    @staticmethod
    def commit() -> None:
        db.session.commit()
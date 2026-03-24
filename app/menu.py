from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class MenuItem:
    key: str
    label: str
    endpoint: Optional[str] = None
    icon: str = ""
    children: List["MenuItem"] = field(default_factory=list)


def get_admin_menu() -> list[MenuItem]:
    return [
        MenuItem(
            key="dashboard",
            label="Dashboard",
            endpoint="dashboard.index",
            icon="dashboard",
        ),
        MenuItem(
            key="administration",
            label="Administration",
            icon="admin",
            children=[
                MenuItem(
                    key="users",
                    label="Users",
                    endpoint="users.list_users",
                    icon="users",
                ),
                MenuItem(
                    key="roles",
                    label="Roles",
                    endpoint="roles.list_roles",
                    icon="shield",
                ),
                MenuItem(
                    key="permissions",
                    label="Permissions",
                    endpoint="roles.permission_catalog",
                    icon="shield",
                ),
                MenuItem(
                    key="settings",
                    label="Settings",
                    endpoint=None,
                    icon="settings",
                ),
            ],
        ),
        MenuItem(
            key="system",
            label="System",
            icon="system",
            children=[
                MenuItem(
                    key="audit",
                    label="Audit & Restore",
                    endpoint=None,
                    icon="history",
                ),
                MenuItem(
                    key="docs",
                    label="Documentation",
                    endpoint=None,
                    icon="docs",
                ),
            ],
        ),
    ]
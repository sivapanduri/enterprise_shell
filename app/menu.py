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
            icon="layout-dashboard",
        ),

        MenuItem(
            key="administration",
            label="Administration",
            icon="settings-2",
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
                    icon="key",
                ),
                MenuItem(
                    key="settings",
                    label="Settings",
                    endpoint="settings.index",
                    icon="settings",
                ),
                MenuItem(
                    key="branding",
                    label="Branding",
                    endpoint="branding.index",
                    icon="palette",
                ),
            ],
        ),

        MenuItem(
            key="system",
            label="System",
            icon="server",
            children=[
                MenuItem(
                    key="audit",
                    label="Audit & Restore",
                    endpoint="audit.list_transactions",
                    icon="history",
                ),
                MenuItem(
                    key="docs",
                    label="Documentation",
                    endpoint=None,
                    icon="book-open",
                ),
            ],
        ),
    ]
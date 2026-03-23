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
    """
    Central menu definition for the authenticated shell.

    Keep this simple in Stage 3.
    In later stages, this same structure can become RBAC-aware
    without rewriting templates.
    """
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
                    endpoint=None,
                    icon="users",
                ),
                MenuItem(
                    key="roles",
                    label="Roles & Permissions",
                    endpoint=None,
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
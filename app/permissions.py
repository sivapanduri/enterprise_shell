"""
Central registry of shell permissions.

Keep these names stable once they are used in migrations, seed data,
roles, and future module checks.
"""

PERMISSIONS = [
    # Dashboard
    ("dashboard.view", "Dashboard", "View the authenticated dashboard"),

    # Users
    ("users.view", "Users", "View users"),
    ("users.create", "Users", "Create users"),
    ("users.edit", "Users", "Edit users"),
    ("users.activate", "Users", "Activate users"),
    ("users.deactivate", "Users", "Deactivate users"),
    ("users.assign_roles", "Users", "Assign roles to users"),
    ("users.reset_password", "Users", "Reset user passwords"),

    # Roles
    ("roles.view", "Roles", "View roles"),
    ("roles.create", "Roles", "Create roles"),
    ("roles.edit", "Roles", "Edit roles"),
    ("roles.assign_permissions", "Roles", "Assign permissions to roles"),

    # Permissions
    ("permissions.view", "Permissions", "View permission catalog"),

    # Settings
    ("settings.view", "Settings", "View settings"),
    ("settings.edit", "Settings", "Edit settings"),

    # Branding
    ("branding.view", "Branding", "View branding"),
    ("branding.edit", "Branding", "Edit branding"),

    # Audit
    ("audit.view", "Audit", "View audit records"),
    ("audit.export", "Audit", "Export audit data"),
    ("audit.restore_preview", "Audit", "Preview restoration plans"),
    ("audit.restore_execute", "Audit", "Execute restoration actions"),

    # Restore
    ("restore.view", "Restore", "View restoration history"),

    # Profile
    ("profile.view", "Profile", "View own profile"),
    ("profile.edit", "Profile", "Edit own profile"),
    ("profile.change_password", "Profile", "Change own password"),

    # Docs
    ("docs.view", "Documentation", "View internal documentation"),
]
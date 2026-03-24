from flask import flash, render_template
from flask_login import current_user

from app.blueprints.branding import branding_bp
from app.forms.branding import LoginBrandingForm, PublicBrandingForm, ThemeBrandingForm
from app.models.branding import BrandingTheme
from app.security.decorators import permission_required
from app.services.branding_service import BrandingService


@branding_bp.get("/")
@permission_required("branding.view")
def index():
    theme = BrandingService.get_or_create_active_theme()
    stats = {
        "total_themes": BrandingTheme.query.count(),
        "active_theme_name": theme.theme_name,
        "primary_color": theme.primary_color,
    }
    return render_template("branding/index.html", stats=stats, theme=theme)


@branding_bp.route("/theme", methods=["GET", "POST"])
@permission_required("branding.edit")
def theme():
    theme = BrandingService.get_or_create_active_theme()
    form = ThemeBrandingForm(obj=theme)

    if form.validate_on_submit():
        BrandingService.save_theme_settings(
            {
                "theme_name": form.theme_name.data.strip(),
                "app_name": form.app_name.data.strip(),
                "app_tagline": form.app_tagline.data.strip(),
                "logo_path": form.logo_path.data.strip(),
                "favicon_path": (form.favicon_path.data or "").strip(),
                "primary_color": form.primary_color.data.strip(),
                "secondary_color": form.secondary_color.data.strip(),
                "accent_color": form.accent_color.data.strip(),
                "sidebar_style": form.sidebar_style.data,
                "navbar_style": form.navbar_style.data,
                "footer_text": form.footer_text.data.strip(),
            },
            updated_by_id=current_user.id,
        )
        flash("Theme settings saved successfully.", "success")

    return render_template("branding/theme.html", form=form)


@branding_bp.route("/login", methods=["GET", "POST"])
@permission_required("branding.edit")
def login_page():
    theme = BrandingService.get_or_create_active_theme()
    form = LoginBrandingForm(obj=theme)

    if form.validate_on_submit():
        BrandingService.save_login_branding(
            {
                "login_title": form.login_title.data.strip(),
                "login_subtitle": form.login_subtitle.data.strip(),
            },
            updated_by_id=current_user.id,
        )
        flash("Login branding saved successfully.", "success")

    return render_template("branding/login.html", form=form)


@branding_bp.route("/public", methods=["GET", "POST"])
@permission_required("branding.edit")
def public_site():
    theme = BrandingService.get_or_create_active_theme()
    form = PublicBrandingForm(obj=theme)

    if form.validate_on_submit():
        BrandingService.save_public_branding(
            {
                "public_hero_title": form.public_hero_title.data.strip(),
                "public_hero_subtitle": form.public_hero_subtitle.data.strip(),
            },
            updated_by_id=current_user.id,
        )
        flash("Public branding saved successfully.", "success")

    return render_template("branding/public.html", form=form)


@branding_bp.get("/preview")
@permission_required("branding.view")
def preview():
    branding = BrandingService.get_effective_branding()
    return render_template("branding/preview.html", branding_preview=branding)
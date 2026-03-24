from flask import flash, render_template
from flask_login import current_user

from app.blueprints.settings import settings_bp
from app.forms.settings import GeneralSettingsForm, SecuritySettingsForm
from app.models.settings import AppSetting
from app.security.decorators import permission_required
from app.services.settings_service import SettingsService


@settings_bp.get("/")
@permission_required("settings.view")
def index():
    stats = {
        "total_settings": AppSetting.query.count(),
        "general_settings": AppSetting.query.filter_by(category="general").count(),
        "security_settings": AppSetting.query.filter_by(category="security").count(),
    }
    return render_template("settings/index.html", stats=stats)


@settings_bp.route("/general", methods=["GET", "POST"])
@permission_required("settings.edit")
def general():
    form = GeneralSettingsForm(data=SettingsService.get_general_settings())

    if form.validate_on_submit():
        SettingsService.save_general_settings(
            {
                "app_display_name": form.app_display_name.data.strip(),
                "app_tagline": form.app_tagline.data.strip(),
                "company_name": form.company_name.data.strip(),
                "support_email": form.support_email.data.strip().lower(),
                "footer_text": form.footer_text.data.strip(),
            },
            updated_by_id=current_user.id,
        )
        flash("General settings saved successfully.", "success")

    return render_template("settings/general.html", form=form)


@settings_bp.route("/security", methods=["GET", "POST"])
@permission_required("settings.edit")
def security():
    form = SecuritySettingsForm(data=SettingsService.get_security_settings())

    if form.validate_on_submit():
        SettingsService.save_security_settings(
            {
                "password_min_length": form.password_min_length.data,
                "session_timeout_minutes": form.session_timeout_minutes.data,
                "remember_me_enabled": form.remember_me_enabled.data,
                "force_password_change_on_first_login": form.force_password_change_on_first_login.data,
            },
            updated_by_id=current_user.id,
        )
        flash("Security settings saved successfully.", "success")

    return render_template("settings/security.html", form=form)
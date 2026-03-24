from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class GeneralSettingsForm(FlaskForm):
    app_display_name = StringField(
        "Application display name",
        validators=[DataRequired(), Length(min=2, max=255)],
    )
    app_tagline = StringField(
        "Application tagline",
        validators=[DataRequired(), Length(min=2, max=255)],
    )
    company_name = StringField(
        "Company name",
        validators=[DataRequired(), Length(min=2, max=255)],
    )
    support_email = StringField(
        "Support email",
        validators=[DataRequired(), Email(), Length(max=255)],
    )
    footer_text = TextAreaField(
        "Footer text",
        validators=[DataRequired(), Length(min=2, max=1000)],
    )
    submit = SubmitField("Save general settings")


class SecuritySettingsForm(FlaskForm):
    password_min_length = IntegerField(
        "Minimum password length",
        validators=[DataRequired(), NumberRange(min=6, max=128)],
    )
    session_timeout_minutes = IntegerField(
        "Session timeout (minutes)",
        validators=[DataRequired(), NumberRange(min=5, max=1440)],
    )
    remember_me_enabled = BooleanField("Enable remember me")
    force_password_change_on_first_login = BooleanField("Force password change on first login")
    submit = SubmitField("Save security settings")
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, Regexp


HEX_COLOR_VALIDATOR = Regexp(
    r"^#[0-9A-Fa-f]{6}$",
    message="Enter a valid hex color like #1f4b99",
)


class ThemeBrandingForm(FlaskForm):
    theme_name = StringField("Theme name", validators=[DataRequired(), Length(min=2, max=120)])
    app_name = StringField("App name", validators=[DataRequired(), Length(min=2, max=255)])
    app_tagline = StringField("App tagline", validators=[DataRequired(), Length(min=2, max=255)])
    logo_path = StringField("Logo path", validators=[DataRequired(), Length(min=2, max=500)])
    favicon_path = StringField("Favicon path", validators=[Optional(), Length(max=500)])
    primary_color = StringField("Primary color", validators=[DataRequired(), HEX_COLOR_VALIDATOR])
    secondary_color = StringField("Secondary color", validators=[DataRequired(), HEX_COLOR_VALIDATOR])
    accent_color = StringField("Accent color", validators=[DataRequired(), HEX_COLOR_VALIDATOR])
    sidebar_style = SelectField(
        "Sidebar style",
        choices=[("dark", "Dark"), ("light", "Light")],
        validators=[DataRequired()],
    )
    navbar_style = SelectField(
        "Navbar style",
        choices=[("light", "Light"), ("dark", "Dark")],
        validators=[DataRequired()],
    )
    footer_text = TextAreaField("Footer text", validators=[DataRequired(), Length(min=2, max=500)])
    submit = SubmitField("Save theme settings")


class LoginBrandingForm(FlaskForm):
    login_title = StringField("Login title", validators=[DataRequired(), Length(min=2, max=255)])
    login_subtitle = TextAreaField("Login subtitle", validators=[DataRequired(), Length(min=2, max=500)])
    submit = SubmitField("Save login branding")


class PublicBrandingForm(FlaskForm):
    public_hero_title = StringField("Public hero title", validators=[DataRequired(), Length(min=2, max=255)])
    public_hero_subtitle = TextAreaField("Public hero subtitle", validators=[DataRequired(), Length(min=2, max=1000)])
    submit = SubmitField("Save public branding")
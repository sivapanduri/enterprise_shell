from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class UserCreateForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=255)],
    )
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=120)],
    )
    first_name = StringField(
        "First name",
        validators=[Optional(), Length(max=120)],
    )
    last_name = StringField(
        "Last name",
        validators=[Optional(), Length(max=120)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8, max=128)],
    )
    is_active = BooleanField("Active", default=True)
    is_superadmin = BooleanField("Super admin")
    must_change_password = BooleanField("Must change password", default=True)
    submit = SubmitField("Create user")


class UserEditForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=255)],
    )
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=120)],
    )
    first_name = StringField(
        "First name",
        validators=[Optional(), Length(max=120)],
    )
    last_name = StringField(
        "Last name",
        validators=[Optional(), Length(max=120)],
    )
    is_active = BooleanField("Active")
    is_superadmin = BooleanField("Super admin")
    must_change_password = BooleanField("Must change password")
    submit = SubmitField("Save changes")


class UserRoleAssignmentForm(FlaskForm):
    role_ids = SelectMultipleField("Roles", coerce=int)
    submit = SubmitField("Save roles")
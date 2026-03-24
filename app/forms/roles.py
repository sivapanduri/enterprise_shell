from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectMultipleField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class RoleForm(FlaskForm):
    name = StringField(
        "System name",
        validators=[DataRequired(), Length(min=2, max=120)],
    )
    label = StringField(
        "Display label",
        validators=[DataRequired(), Length(min=2, max=120)],
    )
    description = TextAreaField(
        "Description",
        validators=[Optional(), Length(max=2000)],
    )
    is_system_role = BooleanField("System role")
    submit = SubmitField("Save role")


class RolePermissionAssignmentForm(FlaskForm):
    permission_ids = SelectMultipleField("Permissions", coerce=int)
    submit = SubmitField("Save permissions")
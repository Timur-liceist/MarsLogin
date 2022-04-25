from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    title = StringField("Title of department", validators=[DataRequired()])
    chief = IntegerField("Id of Chief", validators=[DataRequired()])
    members = StringField("Members", validators=[DataRequired()])
    email = EmailField("Department Email", validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])
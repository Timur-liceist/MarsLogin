from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = TextAreaField('Job Title', validators=[DataRequired()])
    team_leader = IntegerField("Team Leader id", validators=[DataRequired()])
    work_size = IntegerField("Team Leader id", validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    # content = TextAreaField("Содержание")
    is_finished = BooleanField("Is job finished?", validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])
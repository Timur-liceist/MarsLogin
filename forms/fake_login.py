from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class FakeForm(FlaskForm):
    id_astronaut = IntegerField('ID астронавта', validators=[DataRequired()])
    password_astronaut = PasswordField('Пароль астронавта', validators=[DataRequired()])
    id_capitan = IntegerField('Пароль', validators=[DataRequired()])
    password_capitan = PasswordField('Пароль астронавта', validators=[DataRequired()])
    submit = SubmitField('Доступ')
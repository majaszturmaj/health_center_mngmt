from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, BooleanField, TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length

class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(min=1, max=50)])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')


class ReportForm(FlaskForm):
    title = StringField('Tytuł Raportu', validators=[DataRequired()]) 
    mood_level = IntegerField('Poziom Samopoczucia', validators=[DataRequired(), NumberRange(min=1, max=10)])
    anxiety_level = IntegerField('Poziom Lęku', validators=[DataRequired(), NumberRange(min=1, max=10)])
    sleep_quality = SelectField('Jakość Snu', choices=[('good', 'Good'), ('average', 'Average'), ('bad', 'Bad')], validators=[DataRequired()])
    appetite_level = IntegerField('Poziom Apetytu', validators=[DataRequired(), NumberRange(min=1, max=10)])
    medication_adherence = BooleanField('Przyjmowanie Leków ', validators=[DataRequired()])
    psychotic_symptoms = BooleanField('Objawy Psychotyczne', validators=[DataRequired()])
    behavioral_observations = TextAreaField('Obserwacje Behawioralne')
    comments = TextAreaField('Komentarze')
    submit = SubmitField('Submit')

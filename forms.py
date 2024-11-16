from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, BooleanField, TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length


class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(min=1, max=50)])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')


class ReportForm(FlaskForm):
    mood_level = SelectField('Poziom nastroju', 
                           choices=[(str(i), str(i)) for i in range(1, 11)],
                           validators=[DataRequired()])
    anxiety_level = SelectField('Poziom lęku',
                              choices=[(str(i), str(i)) for i in range(1, 11)],
                              validators=[DataRequired()])
    sleep_quality = SelectField('Jakość snu',
                              choices=[('good', 'Dobra'), ('average', 'Średnia'), ('bad', 'Zła')],
                              validators=[DataRequired()])
    appetite_level = SelectField('Apetyt',
                               choices=[(str(i), str(i)) for i in range(1, 11)],
                               validators=[DataRequired()])
    medication_adherence = BooleanField('Przyjmowanie leków')
    psychotic_symptoms = BooleanField('Objawy psychotyczne')
    behavioral_observations = TextAreaField('Obserwacje')
    comments = TextAreaField('Komentarze')

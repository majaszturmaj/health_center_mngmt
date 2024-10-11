from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, BooleanField, TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Length

class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(min=1, max=50)])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')


class ReportForm(FlaskForm):
    mood_level = IntegerField('Mood Level', validators=[DataRequired(), NumberRange(min=1, max=10)])
    anxiety_level = IntegerField('Anxiety Level', validators=[DataRequired(), NumberRange(min=1, max=10)])
    sleep_quality = SelectField('Sleep Quality', choices=[('good', 'Good'), ('average', 'Average'), ('bad', 'Bad')], validators=[DataRequired()])
    appetite_level = IntegerField('Appetite Level', validators=[DataRequired(), NumberRange(min=1, max=10)])
    medication_adherence = BooleanField('Medication Adherence', validators=[DataRequired()])
    psychotic_symptoms = BooleanField('Psychotic Symptoms', validators=[DataRequired()])
    behavioral_observations = TextAreaField('Behavioral Observations')
    comments = TextAreaField('Comments')
    submit = SubmitField('Submit')
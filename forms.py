from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TicketForm(FlaskForm):
    title = StringField('Subject', validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Technical Issue', 'Technical Issue'),
        ('Billing Inquiry', 'Billing Inquiry'),
        ('Feature Request', 'Feature Request'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent')
    ], default='Medium', validators=[DataRequired()])
    submit = SubmitField('Submit Ticket')

class TicketResponseForm(FlaskForm):
    content = TextAreaField('Your Response', validators=[DataRequired()])
    is_internal_note = BooleanField('Internal Note (Agent Only)')
    submit = SubmitField('Add Response')

class AssignAgentForm(FlaskForm):
    agent = SelectField('Assign Agent', coerce=int, validators=[DataRequired()]) # coerce=int to convert value to int
    submit = SubmitField('Assign')

class ChangeStatusForm(FlaskForm):
    status = SelectField('Change Status', choices=[
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Status')
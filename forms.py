from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    department = SelectField('Department', choices=[
        ('', 'Select Department'),
        ('aiml', 'Artificial Intelligence & Machine Learning Engineering'),
        ('csd', 'Computer Science and Design'),
        ('cce', 'Computer and Communication Engineering'),
        ('csbs', 'Computer Science & Engineering(IoT & Cyber Security including Block Chain Technology)'),
        ('cse', 'Computer Science & Engineering'),
        ('ece', 'Electronics & Communication Engineering'),
        ('me', 'Mechanical Engineering'),
        ('sh', 'Science & Humanities')
    ], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])

class ExamForm(FlaskForm):
    title = StringField('Exam Title', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    department = SelectField('Department', choices=[
        ('', 'Select Department'),
        ('aiml', 'Artificial Intelligence & Machine Learning Engineering'),
        ('csd', 'Computer Science and Design'),
        ('cce', 'Computer and Communication Engineering'),
        ('csbs', 'Computer Science & Engineering(IoT & Cyber Security including Block Chain Technology)'),
        ('cse', 'Computer Science & Engineering'),
        ('ece', 'Electronics & Communication Engineering'),
        ('me', 'Mechanical Engineering'),
        ('sh', 'Science & Humanities')
    ], validators=[Optional()])
    semester = StringField('Semester', validators=[Optional(), Length(max=50)], render_kw={'placeholder': 'e.g., 1st Semester, 2nd Semester, etc.'})

class QuestionForm(FlaskForm):
    text = TextAreaField('Question', validators=[DataRequired()])
    answer_key = TextAreaField('Answer Key', validators=[DataRequired()])
    min_word_count = IntegerField('Minimum Word Count', validators=[DataRequired()], default=50)
    max_score = FloatField('Maximum Score', validators=[DataRequired()], default=1.0)
    question_type = SelectField('Question Type', choices=[
        ('text', 'Text Answer'),
        ('mcq', 'Multiple Choice'),
        ('short', 'Short Answer')
    ], default='text')
    order = StringField('Order', default="")

class SubmissionForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired(), Length(max=128)])
    student_id = StringField('Student ID', validators=[DataRequired(), Length(max=64)])
    answer_file = FileField('Answer Paper (PDF/Image)', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Only PDF and image files are allowed!')
    ])

class ManualAnswerForm(FlaskForm):
    answer_text = TextAreaField('Student Answer Text', validators=[DataRequired()])
    question_id = IntegerField('Question ID', validators=[DataRequired()])

class StudentForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired(), Length(max=200)])
    student_id = StringField('Student ID/USN', validators=[DataRequired(), Length(max=100)])
    usn = StringField('University Seat Number (USN)', validators=[Optional(), Length(max=100)])
    department = SelectField('Department', choices=[
        ('', 'Select Department'),
        ('aiml', 'Artificial Intelligence & Machine Learning Engineering'),
        ('csd', 'Computer Science and Design'),
        ('cce', 'Computer and Communication Engineering'),
        ('csbs', 'Computer Science & Engineering(IoT & Cyber Security including Block Chain Technology)'),
        ('cse', 'Computer Science & Engineering'),
        ('ece', 'Electronics & Communication Engineering'),
        ('me', 'Mechanical Engineering'),
        ('sh', 'Science & Humanities')
    ], validators=[Optional()])
    semester = SelectField('Semester', choices=[
        ('', 'Select Semester'),
        ('1', '1st Semester'),
        ('2', '2nd Semester'),
        ('3', '3rd Semester'),
        ('4', '4th Semester'),
        ('5', '5th Semester'),
        ('6', '6th Semester'),
        ('7', '7th Semester'),
        ('8', '8th Semester')
    ], validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=15)])

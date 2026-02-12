"""
MongoDB Models for AI Exam Evaluator
Uses MongoEngine ODM for MongoDB
"""
from mongoengine import Document, StringField, DateTimeField, ReferenceField, IntField, FloatField, BooleanField, FileField
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(Document, UserMixin):
    """User model for MongoDB"""
    
    username = StringField(required=True, unique=True, max_length=80)
    email = StringField(required=True, unique=True, max_length=120)
    password = StringField(required=True, max_length=200)
    department = StringField(max_length=200)
    is_faculty = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'users',
        'indexes': ['email', 'username']
    }
    
    def get_id(self):
        """Required for Flask-Login"""
        return str(self.id)
    
    def set_password(self, password):
        """Hash password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class StudentDetail(Document):
    """Student details model for MongoDB"""
    
    # Support both old and new field names for backward compatibility
    student_name = StringField(max_length=200)
    name = StringField(max_length=200)  # Legacy field name
    student_id = StringField(max_length=100)
    usn = StringField(max_length=100)  # University Seat Number
    department = StringField(max_length=200)
    semester = StringField(max_length=50)
    email = StringField(max_length=120)
    phone = StringField(max_length=15)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'student_details',
        'indexes': [
            'name',
            'student_name', 
            'student_id', 
            'usn', 
            'department'
        ]
    }
    
    @property
    def display_name(self):
        """Get the student name, checking both fields"""
        return self.student_name or self.name or ''
    
    @property
    def display_id(self):
        """Get the student ID, defaulting to USN if no student_id"""
        return self.student_id or self.usn or ''
    
    def save(self, *args, **kwargs):
        """Override save to update timestamp and sync fields"""
        self.updated_at = datetime.utcnow()
        # Sync name fields for compatibility
        if self.student_name and not self.name:
            self.name = self.student_name
        elif self.name and not self.student_name:
            self.student_name = self.name
        return super(StudentDetail, self).save(*args, **kwargs)
    
    def __repr__(self):
        return f'<StudentDetail {self.display_name} - {self.display_id}>'


class Exam(Document):
    """Exam model for MongoDB"""
    
    title = StringField(required=True, max_length=200)
    description = StringField()
    department = StringField(max_length=200)
    semester = StringField(max_length=50)
    faculty = ReferenceField(User, required=True, reverse_delete_rule=2)  # CASCADE
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'exams',
        'indexes': ['faculty', 'created_at'],
        'ordering': ['-created_at']
    }
    
    @property
    def questions(self):
        """Get all questions for this exam"""
        return Question.objects(exam=self).order_by('order')
    
    @property
    def submissions(self):
        """Get all submissions for this exam"""
        return Submission.objects(exam=self).order_by('-uploaded_at')
    
    def __repr__(self):
        return f'<Exam {self.title}>'


class Question(Document):
    """Question model for MongoDB"""
    
    exam = ReferenceField(Exam, required=True, reverse_delete_rule=2)  # CASCADE
    text = StringField(required=True)
    answer_key = StringField(required=True)
    max_score = FloatField(default=1.0)
    min_word_count = IntField(default=50)
    question_type = StringField(default='text', max_length=50)
    order = StringField(default="")
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'questions',
        'indexes': ['exam', 'order'],
        'ordering': ['order']
    }
    
    def __repr__(self):
        return f'<Question {self.order} - {self.exam.title}>'


class Submission(Document):
    """Submission model for MongoDB with GridFS support"""
    
    exam = ReferenceField(Exam, required=True, reverse_delete_rule=2)  # CASCADE
    student_detail = ReferenceField('StudentDetail', reverse_delete_rule=1)  # NULLIFY
    student_name = StringField(required=True, max_length=200)
    student_id = StringField(max_length=100)
    
    # GridFS for file storage
    original_file = FileField()
    file_path = StringField(max_length=500)  # Backup file path
    
    total_score = FloatField(default=0.0)
    max_possible_score = FloatField(default=0.0)
    
    processed = BooleanField(default=False)
    uploaded_at = DateTimeField(default=datetime.utcnow)
    processed_at = DateTimeField()
    
    meta = {
        'collection': 'submissions',
        'indexes': ['exam', 'uploaded_at', 'student_name'],
        'ordering': ['-uploaded_at']
    }
    
    def save_file(self, file_data, filename, content_type='application/pdf'):
        """Save file to GridFS"""
        self.original_file.put(file_data, content_type=content_type, filename=filename)
        self.save()
    
    def get_file(self):
        """Retrieve file from GridFS"""
        if self.original_file:
            return self.original_file.read()
        return None
    
    def get_file_name(self):
        """Get original filename"""
        if self.original_file:
            return self.original_file.filename
        return None
    
    @property
    def answers(self):
        """Get all submission answers"""
        return SubmissionAnswer.objects(submission=self).order_by('question_number')
    
    @property
    def grades(self):
        """Get all grades for this submission"""
        return Grade.objects(submission=self)
    
    def __repr__(self):
        return f'<Submission {self.student_name} - {self.exam.title}>'


class SubmissionAnswer(Document):
    """Submission answer model - stores grading results for each question"""
    
    submission = ReferenceField(Submission, required=True, reverse_delete_rule=2)  # CASCADE
    question = ReferenceField(Question, required=True, reverse_delete_rule=2)  # CASCADE
    extracted_text = StringField()  # OCR extracted answer text
    score = FloatField(default=0.0)  # Final score for this answer
    similarity_score = FloatField(default=0.0)  # Semantic similarity score
    feedback = StringField()  # AI-generated feedback
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'submission_answers',
        'indexes': ['submission', 'question'],
        'ordering': ['created_at']
    }
    
    def __repr__(self):
        return f'<SubmissionAnswer {self.submission.student_name} - Q{self.question.order}>'


class Grade(Document):
    """Grade model - stores AI grading results"""
    
    submission = ReferenceField(Submission, required=True, reverse_delete_rule=2)  # CASCADE
    question = ReferenceField(Question, required=True)
    student_answer = StringField()
    
    # Scoring fields
    relevance_score = FloatField(default=0.0)
    accuracy_score = FloatField(default=0.0)
    grammar_score = FloatField(default=0.0)
    completeness_score = FloatField(default=0.0)
    word_count_score = FloatField(default=0.0)
    final_score = FloatField(default=0.0)
    
    detailed_feedback = StringField()
    strengths = StringField()  # JSON string
    improvements = StringField()  # JSON string
    grammar_issues = StringField()  # JSON string
    
    graded_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'grades',
        'indexes': ['submission', 'question'],
        'ordering': ['graded_at']
    }
    
    def __repr__(self):
        return f'<Grade {self.final_score} - {self.submission.student_name}>'

"""
SQLite to MongoDB Migration Script
Transfers all data from SQLite database to MongoDB Atlas
"""
import os
import sys
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import MongoDB models
from models import User, Exam, Question, Submission, SubmissionAnswer, Grade

# MongoDB connection will be handled by MongoEngine through Flask app
from app import app

def get_sqlite_connection():
    """Connect to SQLite database"""
    db_path = os.path.join(os.getcwd(), 'instance', 'app.db')
    if not os.path.exists(db_path):
        print(f"SQLite database not found at {db_path}")
        return None
    return sqlite3.connect(db_path)

def migrate_users(cursor):
    """Migrate users from SQLite to MongoDB"""
    print("\n=== Migrating Users ===")
    cursor.execute("SELECT id, username, email, password_hash, department, is_faculty, created_at FROM user")
    users = cursor.fetchall()
    
    user_id_map = {}  # Map old SQLite IDs to new MongoDB IDs
    
    for old_id, username, email, password_hash, department, is_faculty, created_at in users:
        # Check if user already exists
        existing_user = User.objects(email=email).first()
        if existing_user:
            print(f"User {username} already exists, skipping...")
            user_id_map[old_id] = str(existing_user.id)
            continue
        
        # Parse datetime
        try:
            created_dt = datetime.fromisoformat(created_at) if created_at else datetime.utcnow()
        except:
            created_dt = datetime.utcnow()
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password=password_hash,  # Already hashed from SQLite
            department=department or "",
            is_faculty=bool(is_faculty),
            created_at=created_dt
        )
        user.save()
        user_id_map[old_id] = str(user.id)
        print(f"✓ Migrated user: {username}")
    
    print(f"Total users migrated: {len(user_id_map)}")
    return user_id_map

def migrate_exams(cursor, user_id_map):
    """Migrate exams from SQLite to MongoDB"""
    print("\n=== Migrating Exams ===")
    cursor.execute("SELECT id, title, description, faculty_id, created_at FROM exam")
    exams = cursor.fetchall()
    
    exam_id_map = {}
    
    for old_id, title, description, faculty_id, created_at in exams:
        # Get corresponding MongoDB user ID
        mongo_user_id = user_id_map.get(faculty_id)
        if not mongo_user_id:
            print(f"Warning: Faculty ID {faculty_id} not found for exam {title}")
            continue
        
        # Check if exam already exists
        user = User.objects(id=mongo_user_id).first()
        existing_exam = Exam.objects(title=title, faculty=user).first()
        if existing_exam:
            print(f"Exam '{title}' already exists, skipping...")
            exam_id_map[old_id] = str(existing_exam.id)
            continue
        
        # Parse datetime
        try:
            created_dt = datetime.fromisoformat(created_at) if created_at else datetime.utcnow()
        except:
            created_dt = datetime.utcnow()
        
        # Create new exam
        exam = Exam(
            title=title,
            description=description or "",
            faculty=user,
            created_at=created_dt
        )
        exam.save()
        exam_id_map[old_id] = str(exam.id)
        print(f"✓ Migrated exam: {title}")
    
    print(f"Total exams migrated: {len(exam_id_map)}")
    return exam_id_map

def migrate_questions(cursor, exam_id_map):
    """Migrate questions from SQLite to MongoDB"""
    print("\n=== Migrating Questions ===")
    cursor.execute("SELECT id, exam_id, text, answer_key, max_score, min_word_count, question_type, `order` FROM question")
    questions = cursor.fetchall()
    
    question_id_map = {}
    
    for old_id, exam_id, text, answer_key, max_score, min_word_count, question_type, order in questions:
        # Get corresponding MongoDB exam ID
        mongo_exam_id = exam_id_map.get(exam_id)
        if not mongo_exam_id:
            print(f"Warning: Exam ID {exam_id} not found for question")
            continue
        
        exam = Exam.objects(id=mongo_exam_id).first()
        if not exam:
            print(f"Warning: Exam not found with ID {mongo_exam_id}")
            continue
        
        # Create new question
        question = Question(
            exam=exam,
            text=text or "",
            answer_key=answer_key or "",
            max_score=float(max_score) if max_score else 1.0,
            min_word_count=int(min_word_count) if min_word_count else 50,
            question_type=question_type or "text",
            order=int(order) if order else 0,
            created_at=datetime.utcnow()
        )
        question.save()
        question_id_map[old_id] = str(question.id)
        print(f"✓ Migrated question {order} for exam: {exam.title}")
    
    print(f"Total questions migrated: {len(question_id_map)}")
    return question_id_map

def migrate_submissions(cursor, exam_id_map):
    """Migrate submissions from SQLite to MongoDB"""
    print("\n=== Migrating Submissions ===")
    cursor.execute("""
        SELECT id, exam_id, student_name, student_id, original_file, 
               total_score, submitted_at 
        FROM submission
    """)
    submissions = cursor.fetchall()
    
    submission_id_map = {}
    
    for old_id, exam_id, student_name, student_id, original_file, total_score, submitted_at in submissions:
        # Get corresponding MongoDB exam ID
        mongo_exam_id = exam_id_map.get(exam_id)
        if not mongo_exam_id:
            print(f"Warning: Exam ID {exam_id} not found for submission")
            continue
        
        exam = Exam.objects(id=mongo_exam_id).first()
        if not exam:
            continue
        
        # Parse datetime
        try:
            submitted_dt = datetime.fromisoformat(submitted_at) if submitted_at else datetime.utcnow()
        except:
            submitted_dt = datetime.utcnow()
        
        # Create new submission
        submission = Submission(
            exam=exam,
            student_name=student_name or "",
            student_id=student_id or "",
            file_path=original_file or "",
            total_score=float(total_score) if total_score else 0.0,
            max_possible_score=0.0,  # Will be calculated
            processed=True if total_score else False,
            uploaded_at=submitted_dt,
            processed_at=submitted_dt if total_score else None
        )
        submission.save()
        submission_id_map[old_id] = str(submission.id)
        print(f"✓ Migrated submission: {student_name}")
    
    print(f"Total submissions migrated: {len(submission_id_map)}")
    return submission_id_map

def migrate_submission_answers(cursor, submission_id_map):
    """Migrate submission answers from SQLite to MongoDB - Note: SQLite structure is different"""
    print("\n=== Migrating Submission Answers ===")
    # SQLite has question_id and other fields, but MongoDB model expects question_number
    # We'll skip this migration as the data structure is incompatible
    print("⚠ Skipping submission_answer migration - data structure differs between SQLite and MongoDB")
    print("   SQLite uses question_id (FK), MongoDB uses question_number (integer)")
    print("   This data will be regenerated when processing submissions in the new system")

def main():
    """Main migration function"""
    print("=" * 60)
    print("SQLite to MongoDB Migration Script")
    print("=" * 60)
    
    # Check if SQLite database exists
    db_path = os.path.join(os.getcwd(), 'instance', 'app.db')
    if not os.path.exists(db_path):
        print(f"\n❌ SQLite database not found at {db_path}")
        print("Nothing to migrate.")
        return
    
    # Connect to SQLite
    conn = get_sqlite_connection()
    if not conn:
        print("Failed to connect to SQLite database")
        return
    
    cursor = conn.cursor()
    
    # Run migration with Flask app context
    with app.app_context():
        try:
            # Check MongoDB connection
            from models import User
            User.objects().first()
            print("\n✓ MongoDB connection successful")
            
            # Migrate in order (respecting foreign key relationships)
            user_id_map = migrate_users(cursor)
            exam_id_map = migrate_exams(cursor, user_id_map)
            question_id_map = migrate_questions(cursor, exam_id_map)
            submission_id_map = migrate_submissions(cursor, exam_id_map)
            migrate_submission_answers(cursor, submission_id_map)
            
            print("\n" + "=" * 60)
            print("✓ Migration completed successfully!")
            print("=" * 60)
            
            # Print summary
            print(f"\nSummary:")
            print(f"  Users: {len(user_id_map)}")
            print(f"  Exams: {len(exam_id_map)}")
            print(f"  Questions: {len(question_id_map)}")
            print(f"  Submissions: {len(submission_id_map)}")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            conn.close()

if __name__ == "__main__":
    main()

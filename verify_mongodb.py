from app import app
from models import User, Exam, Question, Submission

app.app_context().push()

print("=" * 60)
print("MongoDB Data Verification")
print("=" * 60)

print(f"\n📊 Database Statistics:")
print(f"  Users: {User.objects.count()}")
print(f"  Exams: {Exam.objects.count()}")
print(f"  Questions: {Question.objects.count()}")
print(f"  Submissions: {Submission.objects.count()}")

print(f"\n👥 Users:")
for u in User.objects:
    print(f"  - {u.username} ({u.email}) - Dept: {u.department}")

print(f"\n📝 Exams:")
for e in Exam.objects:
    question_count = Question.objects(exam=e).count()
    submission_count = Submission.objects(exam=e).count()
    print(f"  - {e.title} by {e.faculty.username}")
    print(f"    Questions: {question_count}, Submissions: {submission_count}")

print("\n✓ Migration verification complete!")

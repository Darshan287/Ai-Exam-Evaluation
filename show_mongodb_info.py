"""
MongoDB Connection Information
Run this to get the connection details for MongoDB Compass
"""

print("=" * 70)
print("MongoDB COMPASS CONNECTION INFORMATION")
print("=" * 70)

connection_string = " "
database_name = "exam_evaluator"

print(f"\n📌 CONNECTION STRING (copy this):")
print(f"   {connection_string}")

print(f"\n📌 DATABASE NAME (important!):")
print(f"   {database_name}")

print("\n" + "=" * 70)
print("STEPS TO VIEW DATA IN MONGODB COMPASS:")
print("=" * 70)

print("""
1. Open MongoDB Compass

2. Paste this connection string:
   mongodb+srv://sheshagirijoshi18_db_user:Shesha-123-db@myapplicationcluster.kjlncpc.mongodb.net/

3. Click "Connect"

4. After connecting, click on the database named: exam_evaluator

5. You should see these collections:
   - users (2 documents)
   - exams (3 documents) 
   - questions (10 documents)
   - submissions (6 documents)
   - submission_answers (empty - populated during grading)
   - grades (empty - populated during grading)

⚠️  IMPORTANT: Make sure you select the 'exam_evaluator' database,
    not 'admin' or 'test' or any other database!
""")

# Verify connection
print("\n" + "=" * 70)
print("VERIFYING DATA IN MONGODB...")
print("=" * 70)

try:
    from app import app
    from models import User, Exam, Question, Submission
    
    app.app_context().push()
    
    user_count = User.objects.count()
    exam_count = Exam.objects.count()
    question_count = Question.objects.count()
    submission_count = Submission.objects.count()
    
    print(f"\n✅ Connected successfully!")
    print(f"\n📊 Current Data:")
    print(f"   Users: {user_count}")
    print(f"   Exams: {exam_count}")
    print(f"   Questions: {question_count}")
    print(f"   Submissions: {submission_count}")
    
    print(f"\n✅ All data is in MongoDB Atlas!")
    print(f"✅ Use the connection string above in MongoDB Compass")
    print(f"✅ Select database: {database_name}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 70)


from app import app
from models import StudentDetail

with app.app_context():
    try:
        students = StudentDetail.objects()
        count = students.count()
        print(f'Total students in database: {count}')
        
        # Show first 5 students with their display names
        for i, student in enumerate(students[:5]):
            print(f'{i+1}. Name: {student.display_name}, ID: {student.display_id}, USN: {student.usn}')
        
        print('✅ Student model working correctly with existing data')
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()
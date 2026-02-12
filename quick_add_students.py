from app import app
from models import StudentDetail

sample_students = [
    {'student_name': 'John Doe', 'student_id': 'ST001', 'usn': '1KS20CS001', 'department': 'cse', 'semester': '6'},
    {'student_name': 'Jane Smith', 'student_id': 'ST002', 'usn': '1KS20CS002', 'department': 'cse', 'semester': '6'},
    {'student_name': 'Alice Johnson', 'student_id': 'ST003', 'usn': '1KS20AI003', 'department': 'aiml', 'semester': '6'},
    {'student_name': 'Bob Wilson', 'student_id': 'ST004', 'usn': '1KS20AI004', 'department': 'aiml', 'semester': '6'},
    {'student_name': 'Charlie Brown', 'student_id': 'ST005', 'usn': '1KS20EC005', 'department': 'ece', 'semester': '4'},
]

with app.app_context():
    for data in sample_students:
        existing = StudentDetail.objects(student_id=data['student_id']).first()
        if not existing:
            student = StudentDetail(**data)
            student.save()
            print(f'Added: {student.student_name}')
        else:
            print(f'Exists: {data["student_name"]}')
    
    total = StudentDetail.objects().count()
    print(f'Total students: {total}')
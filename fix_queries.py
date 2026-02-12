#!/usr/bin/env python3
"""
Fix all MongoEngine query field names to use ReferenceFields correctly
"""
import re

files_to_fix = [
    'routes/exam_routes.py',
    'routes/report_routes.py'
]

replacements = [
    # Fix Question queries
    (r'Question\.objects\(exam_id=exam_id\)', r'Question.objects(exam=exam)'),
    (r'Question\.objects\(exam_id=([^)]+)\)', r'Question.objects(exam=\1)'),
    
    # Fix Submission queries  
    (r'Submission\.objects\(exam_id=exam_id\)', r'Submission.objects(exam=exam)'),
    (r'Submission\.objects\(exam_id=([^)]+)\)', r'Submission.objects(exam=\1)'),
    
    # Fix SubmissionAnswer queries
    (r'SubmissionAnswer\.objects\(submission_id=submission_id\)', r'SubmissionAnswer.objects(submission=submission)'),
    (r'SubmissionAnswer\.objects\(submission_id=([^)]+)\)', r'SubmissionAnswer.objects(submission=\1)'),
    (r'SubmissionAnswer\.objects\(question_id=question\.id\)', r'SubmissionAnswer.objects(question=question)'),
    (r'SubmissionAnswer\.objects\(question_id=([^)]+)\)', r'SubmissionAnswer.objects(question=\1)'),
    
    # Fix SubmissionAnswer creation
    (r'submission_id=str\(submission\.id\)', r'submission=submission'),
    (r'question_id=str\(question\.id\)', r'question=question'),
    
    # Fix submission.exam_id comparisons
    (r'submission\.exam_id != exam_id', r'str(submission.exam.id) != str(exam.id)'),
    (r'submission\.exam_id == exam_id', r'str(submission.exam.id) == str(exam.id)'),
]

for file_path in files_to_fix:
    print(f"Fixing {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed {file_path}")
        else:
            print(f"ℹ️  No changes needed in {file_path}")
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")

print("\n✅ All files processed!")

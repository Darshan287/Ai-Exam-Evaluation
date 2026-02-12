# MongoDB Compass Connection Guide

## Connection Details

**Connection String:**
```
mongodb+srv://sheshagirijoshi18_db_user:Shesha-123-db@myapplicationcluster.kjlncpc.mongodb.net/
```

**Database Name:** `exam_evaluator`

## Steps to View Data in MongoDB Compass:

1. **Open MongoDB Compass**

2. **Connect using the connection string above**
   - Paste the connection string in the "New Connection" field
   - Click "Connect"

3. **Select the Database**
   - After connecting, you'll see your cluster
   - Look for and click on the database named: **`exam_evaluator`**

4. **View Collections**
   You should see these collections with data:
   - **users** (2 documents)
     - anil (anil632514@gmail.com)
     - Sheshagiri Joshi (sheshagiri2004@gmail.com)
   
   - **exams** (3 documents)
     - BCT
     - E-Waste Management
     - Machine Learning
   
   - **questions** (10 documents)
   
   - **submissions** (6 documents)
   
   - **submission_answers** (may be empty - will be populated during grading)
   
   - **grades** (may be empty - will be populated during grading)

## Troubleshooting:

If you don't see the data:

1. **Check you're in the right database**
   - Make sure you selected `exam_evaluator` database (not `admin` or `test`)
   
2. **Refresh the view**
   - Click the refresh icon in MongoDB Compass
   
3. **Check connection**
   - Verify you're connected to: `myapplicationcluster.kjlncpc.mongodb.net`

## Current Data Summary:
- ✅ 2 Users migrated
- ✅ 3 Exams migrated  
- ✅ 10 Questions migrated
- ✅ 6 Submissions migrated

All data has been successfully migrated from SQLite to MongoDB Atlas!

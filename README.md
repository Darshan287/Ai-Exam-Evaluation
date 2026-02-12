# AIExamEvaluator

Lightweight exam evaluation tool that extracts student answers and grades them.

## Quick setup (Windows / PowerShell)

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies (adjust if you have `requirements.txt` or `pyproject.toml`):

```powershell
pip install -r requirements.txt
# or install packages manually, e.g.:
# pip install google-generativeai pytesseract pdfminer.six
```

3. Set the Gemini API key in the current terminal session (optional — the grader falls back if missing):

```powershell
$env:GEMINI_API_KEY = "AIzaSyCMkXHiRIiRY5WaupfB1wJjJBySgplTeu8"
```

4. Run the app (example):

```powershell
python main.py
```

## Important

- Do NOT commit API keys or other secrets. The code reads `GEMINI_API_KEY` from the environment.
- If you accidentally committed secrets, rotate them immediately and remove them from git history (use BFG or `git filter-repo`).

## GitHub push (PowerShell)

```powershell
cd "c:\Users\Anil Kumar\OneDrive\Desktop\AIExamEvaluator"
# initialize repository
git init
git checkout -b main
git add .
git commit -m "Initial commit"

# create remote on GitHub (replace <username>/<repo>)
git remote add origin https://github.com/<username>/<repo>.git
git push -u origin main
```

If you prefer using the GitHub CLI:

```powershell
gh auth login
gh repo create <repo> --public --source=. --remote=origin --push
```

## Notes

- See `utils/gemini_grading.py` for grade logic; it will use the Gemini API if `GEMINI_API_KEY` is present and configured, otherwise it uses a fallback grader.
- Add a `.env` file locally for convenience but do not commit it.

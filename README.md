# HR Attendance Data Engineering Project

A beginner-friendly, local sandbox project demonstrating CSV extraction and data validation with Python and Pandas. This ZIP currently contains Modules 1 and 2; PostgreSQL loading, transformation, reporting, and GitHub publishing can be added in later modules.

## Requirements

- Windows 10/11
- Python 3.10 or later
- VS Code (recommended)

## Setup in VS Code PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation, run this for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## Run Module 1 + Module 2 with clean source data

```powershell
python main.py
```

The program reads `data/raw/employees.csv` and `data/raw/attendance.csv`, validates them, and writes valid/invalid CSV files plus a summary into `data/processed/`.

Expected clean-data summary:

| Dataset | Total | Valid | Invalid |
|---|---:|---:|---:|
| Employees | 8 | 8 | 0 |
| Attendance | 16 | 16 | 0 |

## Run invalid-data demonstration

```powershell
python run_validation_demo.py
```

The test data intentionally contains missing values, duplicate IDs, invalid salary/date/status values, and unknown employee IDs.

Expected demonstration counts:

| Dataset | Total | Valid | Invalid |
|---|---:|---:|---:|
| Employees | 7 | 1 | 6 |
| Attendance | 10 | 3 | 7 |

A row may contain more than one validation error. The attendance checks compare employee IDs against the valid employee records in the same test batch.

## Run automated tests

```powershell
python -m pytest -v
```

## Project structure

```text
HR_Attendance_Project/
├── data/
│   ├── raw/
│   │   ├── employees.csv
│   │   ├── attendance.csv
│   │   └── test_samples/
│   └── processed/
├── src/
│   ├── __init__.py
│   ├── extraction.py
│   └── validation.py
├── tests/
│   └── test_validation.py
├── main.py
├── run_validation_demo.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Validation rules

- Required columns and non-empty values
- Positive employee and attendance IDs
- Unique employee IDs and attendance IDs
- Numeric, non-negative salary
- Allowed attendance statuses: Present, Absent, Leave
- Parseable attendance dates
- Attendance employee IDs must exist in the valid employee dataset
- No duplicate attendance for the same employee and date

## Important

This is a learning project using fictional sample data. It does not connect to PostgreSQL yet. Database schema creation and loading will be added in a later module. Do not put real employee personal data or database passwords in GitHub.

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EMPLOYEE_FILE = BASE_DIR / "data" / "raw" / "employees.csv"
ATTENDANCE_FILE = BASE_DIR / "data" / "raw" / "attendance.csv"


def extract_employees():
    """Read employee records from the source CSV."""
    try:
        employees = pd.read_csv(EMPLOYEE_FILE)
        print("Employee data extracted successfully!")
        print("Total employee records:", len(employees))
        return employees
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Employee file not found: {EMPLOYEE_FILE}") from exc


def extract_attendance():
    """Read attendance records from the source CSV."""
    try:
        attendance = pd.read_csv(ATTENDANCE_FILE)
        print("Attendance data extracted successfully!")
        print("Total attendance records:", len(attendance))
        return attendance
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Attendance file not found: {ATTENDANCE_FILE}") from exc


def extract_all_data():
    """Extract both employee and attendance datasets."""
    return extract_employees(), extract_attendance()

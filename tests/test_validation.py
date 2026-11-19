import pandas as pd

from src.validation import validate_employees, validate_attendance


def test_employee_validation_separates_invalid_records():
    source = pd.DataFrame([
        {"employee_id": 1, "employee_name": "Asha", "department": "HR", "salary": 30000},
        {"employee_id": 2, "employee_name": "", "department": "IT", "salary": 35000},
    ])
    valid, invalid = validate_employees(source)
    assert len(valid) == 1
    assert len(invalid) == 1
    assert "Missing employee_name" in invalid.iloc[0]["validation_errors"]


def test_attendance_rejects_unknown_employee():
    employees = pd.DataFrame([
        {"employee_id": 1, "employee_name": "Asha", "department": "HR", "salary": 30000}
    ])
    attendance = pd.DataFrame([
        {"attendance_id": 1, "employee_id": 999, "attendance_date": "2026-11-01", "status": "Present"}
    ])
    valid_employees, _ = validate_employees(employees)
    valid, invalid = validate_attendance(attendance, valid_employees)
    assert len(valid) == 0
    assert len(invalid) == 1
    assert "does not exist" in invalid.iloc[0]["validation_errors"]

from pathlib import Path
import pandas as pd

from src.validation import validate_employees, validate_attendance

BASE_DIR = Path(__file__).resolve().parent
TEST_DIR = BASE_DIR / "data" / "raw" / "test_samples"
OUTPUT_DIR = BASE_DIR / "data" / "processed"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    employees = pd.read_csv(TEST_DIR / "employees_invalid.csv")
    attendance = pd.read_csv(TEST_DIR / "attendance_invalid.csv")

    valid_employees, invalid_employees = validate_employees(employees)
    valid_attendance, invalid_attendance = validate_attendance(
        attendance, valid_employees
    )

    results = {
        "demo_valid_employees.csv": valid_employees,
        "demo_invalid_employees.csv": invalid_employees,
        "demo_valid_attendance.csv": valid_attendance,
        "demo_invalid_attendance.csv": invalid_attendance,
    }
    for filename, dataframe in results.items():
        dataframe.to_csv(OUTPUT_DIR / filename, index=False)

    print("\nEMPLOYEE TEST RESULTS")
    print(f"Total: {len(employees)} | Valid: {len(valid_employees)} | Invalid: {len(invalid_employees)}")
    print(invalid_employees[["employee_id", "validation_errors"]].to_string(index=False))

    print("\nATTENDANCE TEST RESULTS")
    print(f"Total: {len(attendance)} | Valid: {len(valid_attendance)} | Invalid: {len(invalid_attendance)}")
    print(invalid_attendance[["attendance_id", "employee_id", "validation_errors"]].to_string(index=False))
    print("\nInvalid-data demonstration completed.")


if __name__ == "__main__":
    main()

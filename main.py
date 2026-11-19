from pathlib import Path
import pandas as pd

from src.extraction import extract_all_data
from src.validation import validate_employees, validate_attendance

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "data" / "processed"


def main():
    print("=" * 48)
    print("HR ATTENDANCE DATA ENGINEERING - MODULE 2")
    print("=" * 48)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    employees, attendance = extract_all_data()
    valid_employees, invalid_employees = validate_employees(employees)
    valid_attendance, invalid_attendance = validate_attendance(
        attendance, valid_employees
    )

    outputs = {
        "valid_employees.csv": valid_employees,
        "invalid_employees.csv": invalid_employees,
        "valid_attendance.csv": valid_attendance,
        "invalid_attendance.csv": invalid_attendance,
    }
    for filename, dataframe in outputs.items():
        dataframe.to_csv(OUTPUT_DIR / filename, index=False)

    summary = pd.DataFrame([
        {
            "dataset": "employees",
            "total_records": len(employees),
            "valid_records": len(valid_employees),
            "invalid_records": len(invalid_employees),
        },
        {
            "dataset": "attendance",
            "total_records": len(attendance),
            "valid_records": len(valid_attendance),
            "invalid_records": len(invalid_attendance),
        },
    ])
    summary.to_csv(OUTPUT_DIR / "validation_summary.csv", index=False)

    print("\nVALIDATION SUMMARY")
    print(summary.to_string(index=False))
    print(f"\nOutput files saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

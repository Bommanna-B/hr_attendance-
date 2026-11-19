import pandas as pd

ALLOWED_ATTENDANCE_STATUS = {"Present", "Absent", "Leave"}


def _add_error(errors, mask, message):
    """Append a message to each row selected by a Boolean mask."""
    for position, selected in enumerate(mask.fillna(False).tolist()):
        if selected:
            errors[position].append(message)


def _missing_mask(series):
    """Treat null values and whitespace-only strings as missing."""
    return series.isna() | series.astype("string").str.strip().eq("").fillna(False)


def validate_employees(employees):
    df = employees.copy()
    required = ["employee_id", "employee_name", "department", "salary"]
    missing_columns = [column for column in required if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing employee columns: {missing_columns}")

    errors = [[] for _ in range(len(df))]

    for column in required:
        _add_error(errors, _missing_mask(df[column]), f"Missing {column}")

    employee_ids = pd.to_numeric(df["employee_id"], errors="coerce")
    _add_error(errors, employee_ids.isna(), "Invalid employee_id type")
    _add_error(errors, employee_ids.notna() & employee_ids.le(0), "Employee ID must be positive")
    _add_error(
        errors,
        employee_ids.notna() & employee_ids.duplicated(keep=False),
        "Duplicate employee_id",
    )

    salary = pd.to_numeric(df["salary"], errors="coerce")
    _add_error(errors, salary.isna() & df["salary"].notna(), "Invalid salary type")
    _add_error(errors, salary.notna() & salary.lt(0), "Salary cannot be negative")

    df["validation_errors"] = ["; ".join(row_errors) for row_errors in errors]
    valid = df.loc[df["validation_errors"].eq("")].copy()
    invalid = df.loc[df["validation_errors"].ne("")].copy()

    if not valid.empty:
        valid["employee_id"] = pd.to_numeric(valid["employee_id"]).astype("int64")
        valid["salary"] = pd.to_numeric(valid["salary"]).astype("float64")

    return valid, invalid


def validate_attendance(attendance, valid_employees):
    df = attendance.copy()
    required = ["attendance_id", "employee_id", "attendance_date", "status"]
    missing_columns = [column for column in required if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing attendance columns: {missing_columns}")

    errors = [[] for _ in range(len(df))]

    for column in required:
        _add_error(errors, _missing_mask(df[column]), f"Missing {column}")

    attendance_ids = pd.to_numeric(df["attendance_id"], errors="coerce")
    _add_error(errors, attendance_ids.isna(), "Invalid attendance_id type")
    _add_error(errors, attendance_ids.notna() & attendance_ids.le(0), "Attendance ID must be positive")
    _add_error(
        errors,
        attendance_ids.notna() & attendance_ids.duplicated(keep=False),
        "Duplicate attendance_id",
    )

    employee_ids = pd.to_numeric(df["employee_id"], errors="coerce")
    _add_error(errors, employee_ids.isna(), "Invalid employee_id type")
    _add_error(errors, employee_ids.notna() & employee_ids.le(0), "Employee ID must be positive")

    valid_employee_ids = set(
        pd.to_numeric(valid_employees["employee_id"], errors="coerce")
        .dropna()
        .astype("int64")
    )
    unknown_employee = employee_ids.notna() & ~employee_ids.isin(valid_employee_ids)
    _add_error(errors, unknown_employee, "Employee ID does not exist in valid employees")

    dates = pd.to_datetime(df["attendance_date"], errors="coerce", format="mixed")
    _add_error(errors, dates.isna(), "Invalid attendance date")

    statuses = df["status"].astype("string").str.strip()
    _add_error(errors, ~statuses.isin(ALLOWED_ATTENDANCE_STATUS), "Invalid attendance status")

    duplicate_key_rows = employee_ids.notna() & dates.notna()
    duplicate_attendance = pd.Series(False, index=df.index)
    if duplicate_key_rows.any():
        keys = pd.DataFrame({
            "employee_id": employee_ids.loc[duplicate_key_rows],
            "attendance_date": dates.loc[duplicate_key_rows],
        })
        duplicate_attendance.loc[duplicate_key_rows] = keys.duplicated(keep=False).to_numpy()
    _add_error(
        errors,
        duplicate_attendance,
        "Duplicate attendance for employee and date",
    )

    df["validation_errors"] = ["; ".join(row_errors) for row_errors in errors]
    valid = df.loc[df["validation_errors"].eq("")].copy()
    invalid = df.loc[df["validation_errors"].ne("")].copy()

    if not valid.empty:
        valid["attendance_id"] = pd.to_numeric(valid["attendance_id"]).astype("int64")
        valid["employee_id"] = pd.to_numeric(valid["employee_id"]).astype("int64")
        valid["attendance_date"] = pd.to_datetime(
            valid["attendance_date"], errors="raise", format="mixed"
        )
        valid["status"] = valid["status"].astype("string").str.strip()

    return valid, invalid

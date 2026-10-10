def validate(row, number):
    if not isinstance(row, dict):
        raise ValueError(f"line {number}: expected object")
    if not isinstance(row.get("tenant"),str) or not isinstance(row.get("id"),str):
        raise ValueError(f"line {number}: tenant and id must be strings")

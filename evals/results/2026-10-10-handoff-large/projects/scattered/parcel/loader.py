import json
from pathlib import Path
from .validation import validate

def load(path):
    records=[]
    for number,line in enumerate(Path(path).read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            row=json.loads(line)
        except json.JSONDecodeError:
            raise ValueError(f"line {number}: invalid JSON")
        validate(row, number)
        records.append(row)
    return records

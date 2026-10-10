import argparse
import json
from pathlib import Path

def read_records(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]

def format_records(records):
    return "\n".join(json.dumps(row, sort_keys=True) for row in records) + ("\n" if records else "")

def nonnegative_int(value):
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid nonnegative integer: {value!r}")
    if number < 0:
        raise argparse.ArgumentTypeError(f"must be a nonnegative integer: {value!r}")
    return number

def limit_records(records, limit=None):
    return records if limit is None else records[:limit]

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--limit", type=nonnegative_int, default=None, metavar="N")
    args = parser.parse_args(argv)
    print(format_records(limit_records(read_records(args.path), args.limit)), end="")

if __name__ == "__main__":
    main()

import argparse
from .service import execute

def nonnegative_int(text):
    try:
        value=int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid nonnegative integer: {text!r}")
    if value<0:
        raise argparse.ArgumentTypeError(f"invalid nonnegative integer: {text!r}")
    return value

def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--tenant", default=None)
    parser.add_argument("--limit", type=nonnegative_int, default=None)
    args=parser.parse_args(argv)
    try:
        output=execute(args.path, tenant=args.tenant, limit=args.limit)
    except ValueError as error:
        parser.error(str(error))
    print(output, end="")
